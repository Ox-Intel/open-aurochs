import { standardDeviation } from "./stats.js";
export function getReportScorecardsByFramework(report) {
  // Aggregate all the scorecards by framework, so we end up with:
  // - frameworks:
  //   - framework
  //   - scorecards
  //   - average_ox_score
  //   - scores_by_criteria
  //     - criteria
  //     - scores
  //     - scoreValues
  //     - average_score
  var obj = {};

  var ox_scores = {};
  var ox_scores_counts = {};
  var has_skipped = false;
  for (var i in report?.scorecards) {
    var sc = report.scorecards[i];

    // This is a scorecard for this framework.  Aggregate it.
    if (obj[sc.framework.id] === undefined) {
      obj[sc.framework.id] = {
        scorecards: [],
        framework: sc.framework,
        average_ox_score: null,
        scores_by_criteria_key: {},
        scores_by_criteria: [],
      };
    }
    obj[sc.framework.id].scorecards.push(sc);
    if (ox_scores[sc.framework.id] == undefined) {
      ox_scores[sc.framework.id] = 0;
    }
    if (ox_scores_counts[sc.framework.id] == undefined) {
      ox_scores_counts[sc.framework.id] = 0;
    }
    ox_scores[sc.framework.id] += Number(sc.ox_score);
    ox_scores_counts[sc.framework.id] += 1;
    if (sc.has_skipped) {
      has_skipped = true;
    }
    for (var c_index in sc.framework?.criteria) {
      var c = sc.framework.criteria[c_index];
      obj[sc.framework.id].scores_by_criteria_key[c.id] = obj[sc.framework.id].scores_by_criteria_key[c.id] || {};
      obj[sc.framework.id].scores_by_criteria_key[c.id].scores =
        obj[sc.framework.id].scores_by_criteria_key[c.id].scores || [];
      obj[sc.framework.id].scores_by_criteria_key[c.id].scoreValues =
        obj[sc.framework.id].scores_by_criteria_key[c.id].scoreValues || [];
      obj[sc.framework.id].scores_by_criteria_key[c.id].total_score =
        obj[sc.framework.id].scores_by_criteria_key[c.id].total_score || 0;

      for (let scs of sc.scores) {
        if (scs.criteria.id == c.id) {
          obj[sc.framework.id].scores_by_criteria_key[c.id].criteria = c;
          obj[sc.framework.id].scores_by_criteria_key[c.id].scores.push(scs);
          if (
            scs.score != "" &&
            scs.score != "null" &&
            scs.score != null &&
            scs.score &&
            (Number(scs.score) || Number(scs.score) === 0)
          ) {
            obj[sc.framework.id].scores_by_criteria_key[c.id].scoreValues.push(Number(scs.score));
            obj[sc.framework.id].scores_by_criteria_key[c.id].total_score += Number(scs.score);
          }
        }
      }
    }

    if (obj[sc.framework.id]) {
      obj[sc.framework.id].has_skipped = has_skipped;
    }
  }
  let criteria_scores = {};
  let criteria_num_scores = {};
  let criteria_possible = {};
  for (let ox_score_f_id in ox_scores) {
    // Need to come back and do this per-criteria.
    for (let c in obj[ox_score_f_id].scores_by_criteria_key) {
      for (let score of obj[ox_score_f_id].scores_by_criteria_key[c].scores) {
        if (!criteria_scores[c]) {
          criteria_scores[c] = 0;
        }
        if (
          score.score != "" &&
          score.score != "null" &&
          score.score != null &&
          score.score &&
          (Number(score.score) || Number(score.score) === 0)
        ) {
          if (!criteria_scores[c]) {
            criteria_scores[c] = 0;
          }
          if (!criteria_num_scores[c]) {
            criteria_num_scores[c] = 0;
          }
          if (!criteria_possible[c]) {
            criteria_possible[c] = 0;
          }
          criteria_scores[c] += Number(score.score);
          criteria_num_scores[c] += 1;
        }
      }
      criteria_possible[c] += 10;
    }
    let total_scores = 0;
    let total_possible = 0;
    for (let c in obj[ox_score_f_id].scores_by_criteria_key) {
      let criteria_sum = 0;
      let criteria_denominator = 0;
      if (c in criteria_num_scores) {
        criteria_sum += criteria_scores[c] / criteria_num_scores[c];
        criteria_denominator += 1;
      }
      if (criteria_denominator > 0) {
        total_scores +=
          (criteria_sum / criteria_denominator) * obj[ox_score_f_id].scores_by_criteria_key[c].criteria.weight;
      }
      total_possible += 10 * obj[ox_score_f_id].scores_by_criteria_key[c].criteria.weight;
    }
    obj[ox_score_f_id].average_ox_score = (100 * total_scores) / total_possible;
    // if (ox_scores_counts[ox_score_f_id] > 0) {
    //   obj[ox_score_f_id].average_ox_score = Number(ox_scores[ox_score_f_id] / ox_scores_counts[ox_score_f_id]).toFixed(
    //     1
    //   );
    // } else {
    //   // obj[sc.framework.id].average_ox_score = 0;
    // }
  }
  for (var f_index in obj) {
    for (c_index in obj[f_index].scores_by_criteria_key) {
      if (
        obj[f_index].scores_by_criteria_key[c_index].scoreValues.length > 0 &&
        (obj[f_index].scores_by_criteria_key[c_index].total_score ||
          obj[f_index].scores_by_criteria_key[c_index].total_score === 0)
      ) {
        obj[f_index].scores_by_criteria_key[c_index].average_score = Number(
          obj[f_index].scores_by_criteria_key[c_index].total_score /
            obj[f_index].scores_by_criteria_key[c_index].scoreValues.length
        ).toFixed(1);
        if (obj[f_index].scores_by_criteria_key[c_index].scoreValues.length > 1) {
          obj[f_index].scores_by_criteria_key[c_index].stddev = standardDeviation(
            obj[f_index].scores_by_criteria_key[c_index].scoreValues
          );
        }
      }
    }
    obj[f_index].scores_by_criteria = Object.values(obj[f_index].scores_by_criteria_key);
    obj[f_index].scores_by_criteria = obj[f_index].scores_by_criteria.sort((a, b) => {
      // return Number(b.criteria.weight) - Number(a.criteria.weight);
      return Number(a.criteria.index) - Number(b.criteria.index);
    });
  }
  return obj;
}
export function getStackScorecardsByFramework(stack) {
  // Aggregate all the scorecards by framework, and average all scores for a report, so we end up with:
  // - frameworks:
  //   - framework
  //   - scorecards (there's one for each report, with an average of all its members)
  //   - average_ox_score  (averaged for all reports)
  //   - scores_by_criteria
  //     - criteria
  //     - scores
  //     - scoreValues
  //     - average_score

  var obj = {};
  for (let report of stack.reports) {
    var ox_scores = {};
    var ox_scores_counts = {};
    for (let sc of report.scorecards) {
      var f = sc?.framework;

      // This is a scorecard for this framework.  Aggregate it.
      if (obj[f.id] === undefined) {
        obj[f.id] = {
          scorecards: [],
          framework: f,
          average_ox_score: null,
          scores_by_criteria_key: {},
          scores_by_criteria: [],
        };
      }

      obj[f.id].scorecards.push(sc);
      if (ox_scores[sc.framework.id] == undefined) {
        ox_scores[sc.framework.id] = 0;
      }
      if (ox_scores_counts[sc.framework.id] == undefined) {
        ox_scores_counts[sc.framework.id] = 0;
      }
      ox_scores[sc.framework.id] += Number(sc.ox_score);
      ox_scores_counts[sc.framework.id] += 1;
      for (var c_index in f?.criteria) {
        var c = f.criteria[c_index];
        obj[f.id].scores_by_criteria_key[c.id] = obj[f.id].scores_by_criteria_key[c.id] || {};
        obj[f.id].scores_by_criteria_key[c.id].scores = obj[f.id].scores_by_criteria_key[c.id].scores || [];
        obj[f.id].scores_by_criteria_key[c.id].scoreValues = obj[f.id].scores_by_criteria_key[c.id].scoreValues || [];
        obj[f.id].scores_by_criteria_key[c.id].total_score = obj[f.id].scores_by_criteria_key[c.id].total_score || 0;

        for (let scs of sc.scores) {
          if (scs.criteria.id == c.id) {
            obj[f.id].scores_by_criteria_key[c.id].criteria = c;
            scs.report = report;
            obj[f.id].scores_by_criteria_key[c.id].scores.push(scs);
            if (
              scs.score != "" &&
              scs.score != "null" &&
              scs.score != null &&
              (Number(scs.score) || Number(scs.score) === 0)
            ) {
              obj[f.id].scores_by_criteria_key[c.id].scoreValues.push(Number(scs.score));
              obj[f.id].scores_by_criteria_key[c.id].total_score += Number(scs.score);
            }
          }
        }
      }
    }

    for (let ox_score_f_id in ox_scores) {
      if (ox_scores_counts[ox_score_f_id] > 0) {
        obj[ox_score_f_id].average_ox_score = Number(
          ox_scores[ox_score_f_id] / ox_scores_counts[ox_score_f_id]
        ).toFixed(1);
      } else {
        // obj[sc.framework.id].average_ox_score = 0;
      }
    }
    for (var f_index in obj) {
      for (c_index in obj[f_index].scores_by_criteria_key) {
        if (
          obj[f_index].scores_by_criteria_key[c_index].scoreValues.length > 0 &&
          (obj[f_index].scores_by_criteria_key[c_index].total_score ||
            obj[f_index].scores_by_criteria_key[c_index].total_score === 0)
        ) {
          obj[f_index].scores_by_criteria_key[c_index].average_score = Number(
            obj[f_index].scores_by_criteria_key[c_index].total_score /
              obj[f_index].scores_by_criteria_key[c_index].scoreValues.length
          ).toFixed(1);
          if (obj[f_index].scores_by_criteria_key[c_index].scoreValues.length > 1) {
            obj[f_index].scores_by_criteria_key[c_index].stddev = standardDeviation(
              obj[f_index].scores_by_criteria_key[c_index].scoreValues
            );
          }
        }
      }
      obj[f_index].scores_by_criteria = Object.values(obj[f_index].scores_by_criteria_key);
      obj[f_index].scores_by_criteria = obj[f_index].scores_by_criteria.sort((a, b) => {
        // return Number(b.criteria.weight) - Number(a.criteria.weight);
        return Number(a.criteria.index) - Number(b.criteria.index);
      });
    }
  }
  return obj;
}
