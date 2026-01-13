import mock
import unittest
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from utils.factory import Factory
from frameworks.models import Criteria, Framework
from organizations.models import (
    Organization,
    Team,
    TeamMember,
    User,
    OrganizationRole,
    GenericPermission,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback

# models_to_test = [
#     Report,
#     Scorecard,
#     Source,
#
#     # These are now dependent on their parent objects, pending more
#     # complex use cases.
#     # ScorecardScore,
#     # SourceFeedback,
# ]


def generalized_two_users_different_orgs(self, cls):
    o1 = Factory.organization()
    o2 = Factory.organization()
    u1, p1 = Factory.user(organization=o1)
    u2, p2 = Factory.user(organization=o2)

    r = getattr(Factory, cls.__name__.lower())(user=u1)
    r.set_permission(
        acting_user=u1,
        user=u1,
        can_score=True,
        can_read=True,
        can_write=True,
        can_administer=True,
    )

    # can permissions
    self.assertTrue(r.can_read(user=u1))
    self.assertFalse(r.can_read(user=u2))

    # queries
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertEqual(cls.authorized_objects.authorize(user=u2).findable.count(), 0)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.all()[0], r)


def generalized_two_teams(self, cls):
    o1 = Factory.organization()
    o2 = Factory.organization()
    t1 = Factory.team(organization=o1)
    t2 = Factory.team(organization=o2)
    u1, p1 = Factory.user(organization=o1, team=t1)
    u2, p2 = Factory.user(organization=o2, team=t2)

    r = getattr(Factory, cls.__name__.lower())(user=u1)
    r.set_permission(
        acting_user=u1,
        team=t1,
        can_score=True,
        can_read=True,
        can_write=True,
        can_administer=True,
    )

    # can permissions
    self.assertTrue(r.can_read(user=u1))
    self.assertFalse(r.can_read(user=u2))

    # queries
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertEqual(cls.authorized_objects.authorize(user=u2).findable.count(), 0)


def generalized_two_users_same_org(self, cls):
    o1 = Factory.organization()
    o2 = Factory.organization()
    t1 = Factory.team(organization=o1)
    t2 = Factory.team(organization=o2)
    u1, p1 = Factory.user(organization=o1, team=t1)
    u2, p2 = Factory.user(organization=o1, team=t2)

    r = getattr(Factory, cls.__name__.lower())(user=u1)
    r.set_permission(
        acting_user=u1,
        organization=o1,
        can_score=True,
        can_read=True,
        can_write=True,
        can_administer=True,
    )

    # can permissions
    self.assertTrue(r.can_read(user=u1))
    self.assertTrue(r.can_read(user=u2))

    # queries
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertEqual(cls.authorized_objects.authorize(user=u2).findable.count(), 1)


def generalized_read_write_administrate(self, cls):
    o1 = Factory.organization()
    o2 = Factory.organization()
    u1, p1 = Factory.user(organization=o1)
    u2, p2 = Factory.user(organization=o2)

    r0 = getattr(Factory, cls.__name__.lower())(user=u1)
    r1 = getattr(Factory, cls.__name__.lower())(user=u1)
    r2 = getattr(Factory, cls.__name__.lower())(user=u1)
    r3 = getattr(Factory, cls.__name__.lower())(user=u1)
    r4 = getattr(Factory, cls.__name__.lower())(user=u1)

    # Give u2 ownership so we're allowed to deauthorize u1.
    r0.set_permission(acting_user=u1, user=u2, can_administer=True)
    r1.set_permission(acting_user=u1, user=u2, can_administer=True)
    r2.set_permission(acting_user=u1, user=u2, can_administer=True)
    r3.set_permission(acting_user=u1, user=u2, can_administer=True)
    r4.set_permission(acting_user=u1, user=u2, can_administer=True)

    r0.set_permission(
        acting_user=u1,
        user=u1,
        can_score=True,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u1,
        user=u1,
        can_score=True,
        can_read=True,
        can_write=False,
        can_administer=False,
    )
    r2.set_permission(
        acting_user=u1,
        user=u1,
        can_score=True,
        can_read=True,
        can_write=True,
        can_administer=False,
    )
    r3.set_permission(
        acting_user=u1,
        user=u1,
        can_score=True,
        can_read=True,
        can_write=True,
        can_administer=True,
    )
    r4.set_permission(
        acting_user=u1,
        user=u1,
        can_score=False,
        can_read=True,
        can_write=False,
        can_administer=False,
    )

    r0 = cls.raw_objects.get(ox_id=r0.ox_id)
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)
    r2 = cls.raw_objects.get(ox_id=r2.ox_id)
    r3 = cls.raw_objects.get(ox_id=r3.ox_id)
    r4 = cls.raw_objects.get(ox_id=r4.ox_id)

    # can permissions
    self.assertTrue(r0.can_know_exists(user=u1))
    self.assertTrue(r0.can_score(user=u1))
    self.assertFalse(r0.can_read(user=u1))
    self.assertFalse(r0.can_write(user=u1))
    self.assertFalse(r0.can_administer(user=u1))

    self.assertTrue(r1.can_know_exists(user=u1))
    self.assertTrue(r1.can_score(user=u1))
    self.assertTrue(r1.can_read(user=u1))
    self.assertFalse(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))

    self.assertTrue(r2.can_know_exists(user=u1))
    self.assertTrue(r2.can_score(user=u1))
    self.assertTrue(r2.can_read(user=u1))
    self.assertTrue(r2.can_write(user=u1))
    self.assertFalse(r2.can_administer(user=u1))

    self.assertTrue(r3.can_know_exists(user=u1))
    self.assertTrue(r3.can_score(user=u1))
    self.assertTrue(r3.can_read(user=u1))
    self.assertTrue(r3.can_write(user=u1))
    self.assertTrue(r3.can_administer(user=u1))

    self.assertTrue(r4.can_know_exists(user=u1))
    self.assertFalse(r4.can_score(user=u1))
    self.assertTrue(r4.can_read(user=u1))
    self.assertFalse(r4.can_write(user=u1))
    self.assertFalse(r4.can_administer(user=u1))

    # queries
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 5)
    self.assertIn(r0, cls.authorized_objects.authorize(user=u1).findable)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertIn(r2, cls.authorized_objects.authorize(user=u1).findable)
    self.assertIn(r3, cls.authorized_objects.authorize(user=u1).findable)
    self.assertIn(r4, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 4)
    self.assertNotIn(r0, cls.authorized_objects.authorize(user=u1).readable)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertIn(r2, cls.authorized_objects.authorize(user=u1).readable)
    self.assertIn(r3, cls.authorized_objects.authorize(user=u1).readable)
    self.assertIn(r4, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 2)
    self.assertIn(r2, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertIn(r3, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 1)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered[0], r3)


def generalized_tiered_overlapping_permissions(self, cls):
    o1 = Factory.organization()
    o2 = Factory.organization()
    t1 = Factory.team(organization=o1)
    # t2 = Factory.team(organization=o2)
    u1, p1 = Factory.user(organization=o1)
    u2, p2 = Factory.user(organization=o2)
    o1.add_user(u1)
    t1.add_user(u1)

    r1 = getattr(Factory, cls.__name__.lower())(user=u1)

    # Give u2 ownership so we're allowed to deauthorize u1.
    r1.set_permission(acting_user=u1, user=u2, can_administer=True)

    # All permissions via layers
    r1.set_permission(
        acting_user=u2,
        user=u1,
        can_score=True,
        can_read=True,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=True,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        organization=o1,
        can_read=False,
        can_write=False,
        can_administer=True,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    self.assertTrue(r1.can_read(user=u1))
    self.assertTrue(r1.can_write(user=u1))
    self.assertTrue(r1.can_administer(user=u1))

    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # No write
    r1.set_permission(
        acting_user=u2,
        user=u1,
        can_score=True,
        can_read=True,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        organization=o1,
        can_score=True,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    self.assertTrue(r1.can_know_exists(user=u1))
    self.assertTrue(r1.can_score(user=u1))
    self.assertTrue(r1.can_read(user=u1))
    self.assertFalse(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # No admin
    r1.set_permission(
        acting_user=u2,
        user=u1,
        can_score=True,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=True,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        organization=o1,
        can_score=True,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    self.assertTrue(r1.can_know_exists(user=u1))
    self.assertTrue(r1.can_score(user=u1))
    self.assertTrue(r1.can_read(user=u1))
    self.assertTrue(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).scoreable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).scoreable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # Read and score from different layers
    r1.set_permission(
        acting_user=u2,
        user=u1,
        can_score=True,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        organization=o1,
        can_score=False,
        can_read=True,
        can_write=False,
        can_administer=False,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    self.assertTrue(r1.can_know_exists(user=u1))
    self.assertTrue(r1.can_score(user=u1))
    self.assertTrue(r1.can_read(user=u1))
    self.assertFalse(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).scoreable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).scoreable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # No read
    r1.set_permission(
        acting_user=u2,
        user=u1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        organization=o1,
        can_score=True,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    self.assertTrue(r1.can_know_exists(user=u1))
    self.assertTrue(r1.can_score(user=u1))
    self.assertFalse(r1.can_read(user=u1))
    self.assertFalse(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).scoreable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).scoreable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # Admin forces all true
    r1.set_permission(
        acting_user=u2,
        user=u1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        organization=o1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=True,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    self.assertTrue(r1.can_know_exists(user=u1))
    self.assertTrue(r1.can_score(user=u1))
    self.assertTrue(r1.can_read(user=u1))
    self.assertTrue(r1.can_write(user=u1))
    self.assertTrue(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).scoreable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).scoreable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # Edit forces all but admin true
    r1.set_permission(
        acting_user=u2,
        user=u1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=True,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u2,
        organization=o1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    self.assertTrue(r1.can_know_exists(user=u1))
    self.assertTrue(r1.can_score(user=u1))
    self.assertTrue(r1.can_read(user=u1))
    self.assertTrue(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).scoreable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).scoreable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)


def generalized_membership_permissions(self, cls):
    o1 = Factory.organization()
    o2 = Factory.organization()
    t1 = Factory.team(organization=o1)
    u1, p1 = Factory.user(organization=o1)
    u2, p2 = Factory.user(organization=o2)

    r1 = getattr(Factory, cls.__name__.lower())(user=u1)

    # Give u2 ownership so we're allowed to deauthorize u1.
    r1.set_permission(acting_user=u1, user=u2, can_administer=True)

    # All permissions via layers
    r1.set_permission(
        acting_user=u1,
        user=u1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u1,
        team=t1,
        can_score=True,
        can_read=True,
        can_write=True,
        can_administer=True,
    )
    r1.set_permission(
        acting_user=u1,
        organization=o1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    # Not a part of anything, no permissions.
    self.assertFalse(r1.can_read(user=u1))
    self.assertFalse(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # Part of team
    t1.add_user(u1)
    u1 = User.objects.get(ox_id=u1.ox_id)
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    # Has permissions
    self.assertTrue(r1.can_read(user=u1))
    self.assertTrue(r1.can_write(user=u1))
    self.assertTrue(r1.can_administer(user=u1))

    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # Removed from team.
    t1.remove_user(u1)
    u1 = User.objects.get(ox_id=u1.ox_id)
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    # No permissions
    self.assertFalse(r1.can_read(user=u1))
    self.assertFalse(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # added back
    t1.add_user(u1)
    u1 = User.objects.get(ox_id=u1.ox_id)
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    # Part of team
    # Has permissions
    self.assertTrue(r1.can_read(user=u1))
    self.assertTrue(r1.can_write(user=u1))
    self.assertTrue(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    t1.remove_user(u1)
    u1 = User.objects.get(ox_id=u1.ox_id)

    # Team permissions methods work.
    self.assertTrue(r1.can_read(team=t1))
    self.assertTrue(r1.can_write(team=t1))
    self.assertTrue(r1.can_administer(team=t1))
    self.assertEqual(cls.authorized_objects.authorize(team=t1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(team=t1).findable)
    self.assertEqual(cls.authorized_objects.authorize(team=t1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(team=t1).readable)
    self.assertEqual(cls.authorized_objects.authorize(team=t1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(team=t1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(team=t1).administered.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(team=t1).administered)

    # Org permissions methods work.
    self.assertFalse(r1.can_read(organization=o1))
    self.assertFalse(r1.can_write(organization=o1))
    self.assertFalse(r1.can_administer(organization=o1))
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).findable.count(), 0
    )
    self.assertNotIn(r1, cls.authorized_objects.authorize(organization=o1).findable)
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).readable.count(), 0
    )
    self.assertNotIn(r1, cls.authorized_objects.authorize(organization=o1).readable)
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).writeable.count(), 0
    )
    self.assertNotIn(r1, cls.authorized_objects.authorize(organization=o1).writeable)
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).administered.count(), 0
    )
    self.assertNotIn(r1, cls.authorized_objects.authorize(organization=o1).administered)

    # Part of org
    o1.add_user(u1)
    u1 = User.objects.get(ox_id=u1.ox_id)
    r1.set_permission(
        acting_user=u1,
        user=u1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u1,
        team=t1,
        can_score=False,
        can_read=False,
        can_write=False,
        can_administer=False,
    )
    r1.set_permission(
        acting_user=u1,
        organization=o1,
        can_score=True,
        can_read=True,
        can_write=True,
        can_administer=True,
    )

    r1 = cls.raw_objects.get(ox_id=r1.ox_id)

    # Has permissions
    self.assertTrue(r1.can_read(user=u1))
    self.assertTrue(r1.can_write(user=u1))
    self.assertTrue(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 1)
    self.assertIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # Removed from org.
    o1.remove_user(u1)
    u1 = User.objects.get(ox_id=u1.ox_id)
    r1 = cls.raw_objects.get(ox_id=r1.ox_id)
    # No permissions
    self.assertFalse(r1.can_know_exists(user=u1))
    self.assertFalse(r1.can_read(user=u1))
    self.assertFalse(r1.can_write(user=u1))
    self.assertFalse(r1.can_administer(user=u1))
    self.assertEqual(cls.authorized_objects.authorize(user=u1).findable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).findable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).readable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).readable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).writeable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(user=u1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(user=u1).administered)

    # Org permissions methods work.
    self.assertTrue(r1.can_know_exists(organization=o1))
    self.assertTrue(r1.can_read(organization=o1))
    self.assertTrue(r1.can_write(organization=o1))
    self.assertTrue(r1.can_administer(organization=o1))
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).findable.count(), 1
    )
    self.assertIn(r1, cls.authorized_objects.authorize(organization=o1).findable)
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).readable.count(), 1
    )
    self.assertIn(r1, cls.authorized_objects.authorize(organization=o1).readable)
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).writeable.count(), 1
    )
    self.assertIn(r1, cls.authorized_objects.authorize(organization=o1).writeable)
    self.assertEqual(
        cls.authorized_objects.authorize(organization=o1).administered.count(), 1
    )
    self.assertIn(r1, cls.authorized_objects.authorize(organization=o1).administered)

    # Team permissions methods work.
    self.assertFalse(r1.can_know_exists(team=t1))
    self.assertFalse(r1.can_read(team=t1))
    self.assertFalse(r1.can_write(team=t1))
    self.assertFalse(r1.can_administer(team=t1))
    self.assertEqual(cls.authorized_objects.authorize(team=t1).findable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(team=t1).findable)
    self.assertEqual(cls.authorized_objects.authorize(team=t1).readable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(team=t1).readable)
    self.assertEqual(cls.authorized_objects.authorize(team=t1).writeable.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(team=t1).writeable)
    self.assertEqual(cls.authorized_objects.authorize(team=t1).administered.count(), 0)
    self.assertNotIn(r1, cls.authorized_objects.authorize(team=t1).administered)


def generalized_permission_exceptions(self, cls):
    o1 = Factory.organization()
    o2 = Factory.organization()
    u1, p1 = Factory.user(organization=o1)
    u2, p2 = Factory.user(organization=o2)

    r1 = getattr(Factory, cls.__name__.lower())(user=u1)

    # Can't remove last permission
    with self.assertRaises(PermissionDenied):
        r1.set_permission(
            acting_user=u1,
            user=u1,
            can_score=False,
            can_read=False,
            can_write=False,
            can_administer=False,
        )

    # Can't set permissions if you're not an admin.
    with self.assertRaises(PermissionDenied):
        r1.set_permission(
            acting_user=u2,
            user=u1,
            can_score=False,
            can_read=False,
            can_write=False,
            can_administer=False,
        )

    # Authorize must be called before create.
    with self.assertRaises(PermissionDenied):
        clone_kwargs = r1.__dict__
        del clone_kwargs["id"]
        del clone_kwargs["_state"]
        del clone_kwargs["created_at"]
        del clone_kwargs["modified_at"]
        del clone_kwargs["created_by_id"]
        del clone_kwargs["modified_by_id"]
        del clone_kwargs["deleted"]
        del clone_kwargs["deleted_at"]
        try:
            del clone_kwargs["_user_1_administer"]
            del clone_kwargs["_user_2_administer"]
            del clone_kwargs["_user_3_administer"]
        except:
            pass
        cls.authorized_objects.deauthorize()
        cls.authorized_objects.create(**clone_kwargs)


class TestFrameworkPermissionsGeneric(TestCase):
    def test_generalized_two_users_different_orgs(self):
        return generalized_two_users_different_orgs(self, Framework)

    def test_generalized_two_teams(self):
        return generalized_two_teams(self, Framework)

    def test_generalized_two_users_same_org(self):
        return generalized_two_users_same_org(self, Framework)

    def test_generalized_read_write_administrate(self):
        return generalized_read_write_administrate(self, Framework)

    def test_generalized_tiered_overlapping_permissions(self):
        return generalized_tiered_overlapping_permissions(self, Framework)

    def test_generalized_membership_permissions(self):
        return generalized_membership_permissions(self, Framework)

    def test_generalized_permission_exceptions(self):
        return generalized_permission_exceptions(self, Framework)


class TestReportPermissionsGeneric(TestCase):
    def test_generalized_two_users_different_orgs(self):
        return generalized_two_users_different_orgs(self, Report)

    def test_generalized_two_teams(self):
        return generalized_two_teams(self, Report)

    def test_generalized_two_users_same_org(self):
        return generalized_two_users_same_org(self, Report)

    def test_generalized_read_write_administrate(self):
        return generalized_read_write_administrate(self, Report)

    def test_generalized_tiered_overlapping_permissions(self):
        return generalized_tiered_overlapping_permissions(self, Report)

    def test_generalized_membership_permissions(self):
        return generalized_membership_permissions(self, Report)

    def test_generalized_permission_exceptions(self):
        return generalized_permission_exceptions(self, Report)


class TestSourcePermissionsGeneric(TestCase):
    def test_generalized_two_users_different_orgs(self):
        return generalized_two_users_different_orgs(self, Source)

    def test_generalized_two_teams(self):
        return generalized_two_teams(self, Source)

    def test_generalized_two_users_same_org(self):
        return generalized_two_users_same_org(self, Source)

    def test_generalized_read_write_administrate(self):
        return generalized_read_write_administrate(self, Source)

    def test_generalized_tiered_overlapping_permissions(self):
        return generalized_tiered_overlapping_permissions(self, Source)

    def test_generalized_membership_permissions(self):
        return generalized_membership_permissions(self, Source)

    def test_generalized_permission_exceptions(self):
        return generalized_permission_exceptions(self, Source)
