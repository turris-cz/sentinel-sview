function draw_map(elem_handler, scores, label) {
    $(elem_handler).vectorMap({
        map: "world_mill",
        backgroundColor: "transparent",
        regionStyle: {
            initial: {
                fill: "#6c757d",
                "fill-opacity": 0.9,
                stroke: "none",
                "stroke-width": 0,
                "stroke-opacity": 1,
            },
            hover: {
                "fill-opacity": 0.8,
                cursor: "default",
            },
        },
        series: {
            regions: [
                {
                    values: scores,
                    scale: ["#C8EEFF", "#0071A4"],
                    normalizeFunction: "polynomial",
                },
            ],
        },
        onRegionTipShow: function (e, el, code) {
            if (scores[code]) {
                el.html(el.html() + " (" + scores[code] + " " + label + ")");
            } else {
                el.html(el.html());
            }
        },
    });
}

/**
 * Clear polling interval for given resource name.
 */
function clear_interval(resource_name) {
    if (!(resource_name in intervals)) {
        return;
    }
    window.clearInterval(intervals[resource_name]);
    delete intervals[resource_name];
}

/**
 * Prepare the page for diplaying data set according
 * to a new settings - such a period or so passed in
 * params
 */
function process_new_settings(api_url, resource_names, params) {
    set_param_in_window_location("period", params["period"]);
    start_multi_poller(api_url, resource_names, params);
}

function set_param_in_window_location(key, value) {
    var url = new URL(document.location.href);
    url.searchParams.set(key, value);
    url_params_string = url.search;
    history.replaceState(null, null, url_params_string);
}

function request_missing_resources(resource_names, resources, url, params) {
    requested_resources = [];
    for (var i = 0; i < resource_names.length; i++) {
        if (resources[resource_names[i]] === null) {
            requested_resources.push(resource_names[i]);
        }
    }
    if (requested_resources.length != 0) {
        start_multi_poller(url, requested_resources, params);
    }
}

/**
 * Start multiple resource pollers ot once.
 */
function start_multi_poller(url, resource_names, params) {
    for (var i = 0; i < resource_names.length; i++) {
        show_spinner(resource_names[i]);
        clear_interval(resource_names[i]);
        resource_poll(url, resource_names[i], params);
        var interval = window.setInterval(
            resource_poll,
            1000,
            url,
            resource_names[i],
            params
        );
        intervals[resource_names[i]] = interval;
    }
}

function show_spinner(resource_name) {
    spinner = document.getElementById("spinner-" + resource_name);
    if (spinner) {
        spinner.style.display = "flex";
    }
}

function hide_spinner(resource_name) {
    spinner = document.getElementById("spinner-" + resource_name);
    if (spinner) {
        spinner.style.display = "none";
    }
}

function resource_poll(url, resource_name, params) {
    $.ajax({
        method: "GET",
        url: url,
        success: process_response,
        data: Object.assign({ name: resource_name }, params),
    });
}

function process_response(response) {
    console.log(response);
    if ("error" in response) {
        console.log("Error occured in server response:");
        console.log(response);
        return;
    }

    if (!("resource_name" in response)) {
        console.log("Missing resource name in server response:");
        console.log(response);
        return;
    }

    if (!(response["resource_name"] in redraw_callbacks)) {
        console.log("Invalid resource name: " + response["resource_name"]);
        if (response["resource_name"] in intervals) {
            clear_interval(response["resource_name"]);
        }
        return;
    }

    if (!response["data"]) {
        // Data are not ready yet.
        return;
    }

    clear_interval(response["resource_name"]);
    hide_spinner(response["resource_name"]);
    redraw_callbacks[response["resource_name"]](response);
}

function createCountryRow(row) {
    td = document.createElement("td");
    let span = document.createElement("span");
    span.className = "flag-icon flag-icon-" + row["country"].toLowerCase();
    span.style.paddingRight = "40px";
    td.appendChild(span);
    let strong = document.createElement("strong");
    strong.innerHTML = row["country"];
    td.appendChild(strong);

    return [td];
}

function createPasswordRow(row) {
    td = document.createElement("td");
    let strong = document.createElement("strong");
    let a = document.createElement("a");
    a.setAttribute("href", "/passwords/details/" + btoa(row["password"]));
    a.innerHTML = row["password"];
    strong.appendChild(a);
    td.appendChild(strong);

    return [td];
}

function createIncidentTypeRow(row) {
    td = document.createElement("td");
    let strong = document.createElement("strong");
    strong.innerHTML = row["source"].concat(" / ").concat(row["action"]);
    td.appendChild(strong);

    return [td];
}

function createUsernameRow(row) {
    td = document.createElement("td");
    let strong = document.createElement("strong");
    strong.innerHTML = row["username"];
    td.appendChild(strong);

    return [td];
}

function createPortRow(row) {
    td = document.createElement("td");
    let strong = document.createElement("strong");
    strong.innerHTML = row["port"];
    td.appendChild(strong);

    return [td];
}

function createIPRow(row) {
    td = document.createElement("td");
    let strong = document.createElement("strong");
    let a = document.createElement("a");
    a.setAttribute("href", "/attackers/details/ip/" + row["ip"]);
    a.innerHTML = row["ip"];
    strong.appendChild(a);
    td.appendChild(strong);

    return [td];
}

function createCombinedRow(row) {
    return createUsernameRow(row).concat(createPasswordRow(row));
}

function create_table(rows, createRow) {
    let table = document.createElement("table");
    table.className = "table table-borderless table-sm table-hover";
    for (var i = 0; i < rows.length; i++) {
        let tr = document.createElement("tr");
        let td = document.createElement("td");
        td.innerHTML = i + 1 + ".";
        tr.appendChild(td);

        tds = createRow(rows[i]);
        for (var j = 0; j < tds.length; j++) {
            tr.appendChild(tds[j]);
        }

        td = document.createElement("td");
        td.innerHTML = rows[i]["count"];
        tr.appendChild(td);

        table.appendChild(tr);
    }
    return table;
}

function insert_no_data_infobox(el) {
    var div = document.createElement("div");
    div.setAttribute(
        "style",
        "display:flex;height:70px;width:100%;align-items:center;justify-content:center"
    );

    var strong = document.createElement("strong");
    strong.innerHTML = "No data available from this period.";

    div.appendChild(strong);
    el.appendChild(div);
}

function create_data_box(data, row_function) {
    var resource_name = data["resource_name"];
    var container = document.getElementById(resource_name);
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    if (data["data"].length != 0) {
        let table = create_table(data["data"], row_function);
        container.appendChild(table);
    } else {
        insert_no_data_infobox(container);
    }
}

function draw_graph(id, data, ykeys, labels) {
    graph_div = document.getElementById(id);
    while (graph_div.firstChild) {
        graph_div.removeChild(graph_div.firstChild);
    }
    if (data === undefined || data.length == 0) {
        insert_no_data_infobox(graph_div);
    } else {
        create_graph(id, "bucket", ykeys, labels, data);
    }
}

function create_graph(id, xkey, ykeys, labels, data) {
    return Morris.Line({
        element: id,
        smooth: false,
        xkey: xkey,
        ykeys: ykeys,
        labels: labels,
        resize: true,
        data: data,
        hideHover: "auto",
    });
}

intervals = {};
redraw_callbacks = {
    all_countries_by_incidents_list: function (data) {
        $("#" + data["resource_name"])
            .contents()
            .remove();
        draw_map("#" + data["resource_name"], data["data"], "incidents");
    },
    all_countries_by_attackers_list: function (data) {
        $("#" + data["resource_name"])
            .contents()
            .remove();
        draw_map("#" + data["resource_name"], data["data"], "attackers");
    },
    all_attackers_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"],
            ["count"],
            ["Unique IP addresses"]
        );
    },
    all_incidents_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"],
            ["count"],
            ["Incidents"]
        );
    },
    my_all_incidents_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"],
            ["count"],
            ["Incidents"]
        );
    },
    all_ports_by_scans_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"],
            ["count"],
            ["Scanned ports"]
        );
    },
    selected_attacker_incidents_graph: function (data) {
        draw_graph(data["resource_name"], data["data"], ["count"], ["Events"]);
    },
    top_countries_by_attackers_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    top_countries_by_incidents_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    top_traps_by_incidents_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    my_top_countries_by_incidents_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    my_top_traps_by_incidents_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    top_actions_by_incidents_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    top_ports_by_scans_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    top_passwords_by_usages_graph: function (data) {
        draw_graph(
            data["resource_name"],
            data["data"]["data"],
            data["data"]["ykeys"],
            data["data"]["labels"]
        );
    },
    selected_password_by_usages_graph: function (data) {
        draw_graph(data["resource_name"], data["data"], ["count"], ["IPs"]);
    },
    top_countries_by_incidents_list: function (data) {
        create_data_box(data, createCountryRow);
    },
    top_countries_by_incidents_list_long: function (data) {
        create_data_box(data, createCountryRow);
    },
    top_countries_by_attackers_list: function (data) {
        create_data_box(data, createCountryRow);
    },
    top_countries_by_attackers_list_long: function (data) {
        create_data_box(data, createCountryRow);
    },
    top_passwords_by_usages_list: function (data) {
        create_data_box(data, createPasswordRow);
    },
    top_incident_types_by_incidents_list: function (data) {
        create_data_box(data, createIncidentTypeRow);
    },
    top_passwords_by_usages_list_long: function (data) {
        create_data_box(data, createPasswordRow);
    },
    top_usernames_by_usages_list_long: function (data) {
        create_data_box(data, createUsernameRow);
    },
    top_ports_by_scans_list_long: function (data) {
        create_data_box(data, createPortRow);
    },
    logins_of_password_by_usages_list: function (data) {
        create_data_box(data, createUsernameRow);
    },
    top_attackers_by_incidents_list_long: function (data) {
        create_data_box(data, createIPRow);
    },
    top_combinations_by_usages_list_long: function (data) {
        create_data_box(data, createCombinedRow);
    },
};

const basicScrollTop = function () {
    const toTopBtn = document.querySelector("#goTop");

    const btnReveal = function () {
        if (window.scrollY >= 300) {
            toTopBtn.classList.add("is-visible");
        } else {
            toTopBtn.classList.remove("is-visible");
        }
    };

    const scrollToTop = function () {
        if (window.scrollY != 0) {
            setTimeout(function () {
                window.scrollTo(0, window.scrollY - 30);
                scrollToTop();
            }, 5);
        }
    };

    window.addEventListener("scroll", btnReveal);
    toTopBtn.addEventListener("click", scrollToTop);
};
