import { find_get_parameter } from "./utils.js";

let page_info_json;
let infinite_scroll_div;
let earliest_comic_loaded = null;
let latest_comic_loaded = null;
let current_page = null;
let num_pages_to_load = 2;
let initializing = true;
let loading_more_pages = false;
// If a page is within these many pixels of the top of the viewport (by percentage of current viewport height),
// it counts as being "viewed" for the purposes of determining what the current viewed page is.
let viewed_page_top_margin_percentage = 0.30;
let load_next_pages_threshold = 1000;

export async function load_page() {
    initializing = true;
    await fetch_all_json_data();
    infinite_scroll_div = document.getElementById("infinite-scroll");
    load_and_go_to_page();
    document.getElementById("load-older-button").onclick = load_older_pages;
    document.getElementById("load-newer-button").onclick = load_newer_pages;
    window.onscroll = on_scroll;
    // document.addEventListener("keydown", event => {
    //     if (event.code === "KeyL") {
    //         set_current_page(get_current_page(current_page, true));
    //     }
    // });
    for (let link of document.getElementsByClassName("chapter-links")) {
        link.addEventListener("click", function () {
            let url = this.getAttribute("href");
            console.log(url);
            window.location.href = url;
            initializing = true;
            infinite_scroll_div.textContent = '';
            load_and_go_to_page();
            initializing = false;
        })
    }
    initializing = false;
}

async function fetch_all_json_data() {
    let response = await fetch("./comic/page_info_list.json");
    console.log("Fetched page info list");
    let json = await response.json();
    page_info_json = json["page_info_list"];
}

function load_and_go_to_page() {
    get_starting_page();
    load_newer_pages();
    go_to_anchor();
}

function get_starting_page() {
    earliest_comic_loaded = 0;
    latest_comic_loaded = -1;
    if (!window.location.href.includes("#")) {
        return;
    }
    let page_name = window.location.href.split("#")[1];
    console.log("Loading page named " + page_name);
    for (let i=0; i < page_info_json.length; i++) {
        console.log(page_info_json[i].page_name);
        if (page_info_json[i].page_name === page_name) {
            console.log("Starting on page " + i);
            if (i !== 0) {
                document.getElementById("load-older").hidden = false;
            }
            earliest_comic_loaded = i;
            latest_comic_loaded = i - 1;
            return;
        }
    }
    console.log("Couldn't find page named " + page_name);
}

function build_comic_div(page) {
    let node = document.createElement("div");
    node.className = "infinite-page";
    node.id = page["page_name"];

    let link_node = document.createElement("a");
    link_node.href = "comic/" + page["page_name"] + ".html";

    let image_node = document.createElement("img");
    image_node.className = "infinite-page-image";
    console.log("Adding div for page " + page["page_name"]);
    image_node.src = "your_content/comics/" + page["page_name"] + "/" + page["Filename"];
    image_node.title = page["Alt text"];

    link_node.appendChild(image_node);
    node.appendChild(link_node);
    return node;
}

function load_older_pages() {
    if (earliest_comic_loaded <= 0) {
        // No more pages to display
        return;
    }
    if (loading_more_pages)
        return;
    loading_more_pages = true;
    try {
        for (let i = 0; i < num_pages_to_load; i++) {
            earliest_comic_loaded--;
            current_page++;

            let node = build_comic_div(page_info_json[earliest_comic_loaded]);
            infinite_scroll_div.insertBefore(node, infinite_scroll_div.firstChild);

            if (earliest_comic_loaded <= 0) {
                // No more pages to display
                document.getElementById("load-older").hidden = true;
                break;
            }
        }
    } finally {
        loading_more_pages = false;
    }
}

function load_newer_pages() {
    if (latest_comic_loaded + 1 >= page_info_json.length) {
        // No more pages to display
        return;
    }
    if (loading_more_pages)
        return;
    loading_more_pages = true;
    document.getElementById("loading-infinite-scroll").hidden = true;
    try {
        for (let i = 0; i < num_pages_to_load; i++) {
            latest_comic_loaded++;

            let node = build_comic_div(page_info_json[latest_comic_loaded]);
            infinite_scroll_div.appendChild(node);

            if (latest_comic_loaded + 1 >= page_info_json.length) {
                // No more pages to display
                document.getElementById("load-newer").hidden = true;
                document.getElementById("caught-up-notification").hidden = false;
                break;
            }
        }
        console.log("Done loading images");
    } finally {
        loading_more_pages = false;
    }
}

function go_to_anchor() {
    if (!window.location.href.includes("#")) {
        return;
    }
    let anchor = window.location.href.split("#")[1];
    let top = document.getElementById(anchor).offsetTop;
    window.scrollTo(0, top);
}

function get_current_page(start_at_page, show_logs=false) {
    if (start_at_page === null) {
        start_at_page = 0;
    }
    let child_nodes = infinite_scroll_div.childNodes;
    let threshold = viewed_page_top_margin_percentage * window.innerHeight;
    if (show_logs) {
        console.log("childNodes length: " + child_nodes.length);
        console.log(threshold);
    }
    for (let i=start_at_page; i < child_nodes.length; i++) {
        let rect = child_nodes[i].getBoundingClientRect();
        if (show_logs)
            console.log("id=" + child_nodes[i].id + ", top=" + rect.top);
        if (rect.top >= threshold) {
            return Math.max(0, i - 1);
        }
    }
    return child_nodes.length - 1;
}

function set_current_page(new_current_page) {
    current_page = new_current_page;
    console.log("Current page: " + current_page);
    let anchor = infinite_scroll_div.childNodes[current_page].id;
    console.log("Anchor: " + anchor);
    let new_url = window.location.href.split("#")[0] + "#" + anchor;
    window.history.replaceState(null, null, new_url);
}

function on_scroll(event) {
    if (initializing) {
        return;
    }
    if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - load_next_pages_threshold) {
        load_newer_pages();
    }

    let new_current_page = get_current_page(current_page);
    if (current_page !== new_current_page) {
        set_current_page(new_current_page);
    }
}
