import "regenerator-runtime/runtime";

export const postToAPI = async function (data, url, store) {
  const unescape_obj = (obj) => {
    var i;
    if (typeof obj == "string") {
      if (obj.indexOf("__AUROCHS_START_PARSER_") !== -1) {
        // Unescape this.
        var parts = obj
          .replace("__AUROCHS_START_PARSER_", "")
          .replace("__AUROCHS_END_PARSER_", "")
          .split("_AUROCHS_MID_");
        return window.aurochs.data[parts[0]][parts[1]];
      } else {
        return obj;
      }
    } else if (obj instanceof Array) {
      var ret_list = [];
      for (i in obj) {
        ret_list.push(unescape_obj(obj[i]));
      }
      return ret_list;
    } else if (obj instanceof Object) {
      var ret_dict = {};
      for (i in obj) {
        ret_dict[i] = unescape_obj(obj[i]);
      }
      return ret_dict;
    }
    return obj;
  };
  const unescape_dict = (dict) => {
    var d = {};
    for (var k in dict) {
      d[k] = unescape_obj(dict[k]);
    }
    return d;
  };
  const updateState = (model, pk, value) => {
    // console.log(model)
    // console.log(pk)
    // console.log(value)
    try {
      if (value.indexOf("|| {}") === -1) {
        store[model] = store[model] || {};
        store[model][pk] = store[model][pk] || {};
        window.aurochs.data[model] = window.aurochs.data[model] || {};
        // console.log(unescape_dict(JSON.parse(value.replace(/window.aurochs.data.(\w+)\['([A-z0-9]+)'\]/g, '"__AUROCHS_START_PARSER_$1_AUROCHS_MID_$2__AUROCHS_END_PARSER_"'))))
        var newVal = unescape_dict(
          JSON.parse(
            value.replace(
              /window.aurochs.data.(\w+)\['([A-z0-9]+)'\]/g,
              '"__AUROCHS_START_PARSER_$1_AUROCHS_MID_$2__AUROCHS_END_PARSER_"'
            )
          )
        );
        if (store[model][pk] != newVal) {
          store[model][pk] = newVal;
          window.aurochs.data[model][pk] = store[model][pk];
          // Handle the current user
          if (model == "users" && pk == store.user.id) {
            store.user = store[model][pk];
            window.aurochs.data.user = store.user;
          }
        }
      } else {
        if (model && pk) {
          store[model] = store[model] || {};
          store[model][pk] = store[model][pk] || {};
        }
      }
      return { ...store };
    } catch (e) {
      // Handles errors (logout, etc) without taking down the app.
      return store;
    }
  };

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify(data),
  });
  const status = await response.status;
  if (status == 200) {
    const data_str = await response.text();

    // try {
    var d = JSON.parse(JSON.parse(data_str));
    // }
    // catch (err) {
    //   console.log(data_str);
    // }

    // Parse response, update window.aurochs.data
    // console.log(d)
    if (d.success) {
      for (var i in d["objs"]) {
        for (var k in d["objs"][i]) {
          // console.log(k)
          // console.log(d["objs"][i])

          if (k && d["objs"][i][k]) {
            var model = k.replace("window.aurochs.data.", "");
            if (model.indexOf("[") !== -1) {
              // We got data for an object.
              var pk = model.substring(model.indexOf("['") + 2, model.indexOf("']"));
              model = model.substring(0, model.indexOf("['"));
              if (d["objs"][i][k].charAt(d["objs"][i][k].length - 1) === ";") {
                d["objs"][i][k] = d["objs"][i][k].substring(0, d["objs"][i][k].length - 1);
              }
              if (d["objs"][i][k] && d["objs"][i][k] != "") {
                updateState(model, pk, d["objs"][i][k]);
              }
            } else {
              // We got a scoping statement.
              updateState(model, false, "store." + model + " || {}");
            }
          }
        }
      }
    } else {
      // console.log("Error:" + d.error_message);
      // console.log(data);
    }
    for (var delete_index in d["deleted"]) {
      var obj = d["deleted"][delete_index];
      if (store[obj.type] && store[obj.type][obj.pk]) {
        delete store[obj.type][obj.pk];
      }
      if (window.aurochs.data[obj.type] && window.aurochs.data[obj.type][obj.pk]) {
        delete window.aurochs.data[obj.type][obj.pk];
      }
    }
    if (d?.objs && Object.keys(d.objs).length > 0) {
      window.aurochs.emitter.emit("reindexSearch");
    }
    return d;
  } else {
    // We didn't get a 200. Skip it, maybe handle this down the road, depending
    // on how complex the race conditions are.
  }
};

export const sendEvent = async function (event_type, data, aurochsData) {
  data["event_type"] = event_type;
  let api_response = await postToAPI(data, window.aurochs.urls.event, aurochsData);
  // console.log(api_response);
  return api_response;
};
export const sendSocketEvent = async function (event_type, data, aurochsData, socket) {
  data["event_type"] = event_type;
  socket.sendObj(data);
  // const api_response = await postToAPI(data, window.aurochs.urls.event, aurochsData);
  // return api_response;
};
