function checkForSlot(target, user, slot) {
  for (let p in target?.permissions) {
    if (p.substring(0, 1) == "U") {
      // 0100 - Score|Read|Write|Admin
      if (p.substring(2) == user.id && target.permissions[p].substring(slot + 0, slot + 1) == "1") {
        return true;
      }
    }
    if (p.substring(0, 1) == "T") {
      for (let t of user.teams) {
        if (p.substring(2) == t.id && target.permissions[p].substring(slot + 0, slot + 1) == "1") {
          return true;
        }
      }
    }
    if (p.substring(0, 1) == "O") {
      for (let o of user.organizations) {
        if (p.substring(2) == o.id && target.permissions[p].substring(slot + 0, slot + 1) == "1") {
          return true;
        }
      }
    }
  }
  return false;
}

export function checkCanScore(target, user) {
  return checkForSlot(target, user, 0);
}
export function checkCanView(target, user) {
  return checkForSlot(target, user, 1);
}
export function checkCanEdit(target, user) {
  return checkForSlot(target, user, 2);
}
export function checkCanManage(target, user) {
  return checkForSlot(target, user, 3);
}
export function checkCanSee(target, user) {
  return (
    checkCanView(target, user) ||
    checkCanEdit(target, user) ||
    checkCanScore(target, user) ||
    checkCanManage(target, user)
  );
}

export function getRoleFromPermissionsString(s, aurochsData) {
  if (s.substring(0, 2) == "U-") {
    return aurochsData.users[s.substring(2)];
  }
  if (s.substring(0, 2) == "T-") {
    return aurochsData.teams[s.substring(2)];
  }
  if (s.substring(0, 2) == "O-") {
    // console.log(aurochsData);
    return aurochsData.organizations[s.substring(2)];
  }
}
export function getPermissionsDictFromAccessString(s) {
  return {
    score: s.substring(0, 1) == "1",
    read: s.substring(1, 2) == "1",
    write: s.substring(2, 3) == "1",
    administer: s.substring(3) == "1",
  };
}
