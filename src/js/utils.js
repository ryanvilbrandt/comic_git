export function ajax_call(url, func, params=null) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        switch (this.readyState) {
            case 0:
                break;
            case 1:
                console.log("Ajax opened " + url);
                break;
            case 2:
                console.log("Ajax status/headers received " + this.status + " / " + this.getAllResponseHeaders());
                break;
            case 3:
                console.log("Ajax loading response text");
                break;
            case 4:
                if (this.status === 200) {
                    func(this);
                } else {
                    console.log("Ajax error: " + this.status + " / " + this.error());
                }
                break;
            default:
        }
    };
    xhttp.open(params === null ? "GET" : "POST", url, true);
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    if (params === null) {
        xhttp.send();
    } else {
        let post_params;
        if (typeof params === "string") {
            post_params = params;
        } else {
            post_params = Object.keys(params).map(
                k => encodeURIComponent(k) + "=" + encodeURIComponent(params[k])
            ).join("&");
        }
        xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhttp.send(post_params);
    }
}

export function title_case(s) {
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}

export function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue + ";";
}

export function getCookie(cname) {
  const name = cname + "=";
  const ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// https://stackoverflow.com/questions/5448545/how-to-retrieve-get-parameters-from-javascript
export function find_get_parameter(parameter_name) {
    let result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
            tmp = item.split("=");
            if (tmp[0] === parameter_name) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

export function init_accordions() {
    let acc = document.getElementsByClassName("accordion-button");
    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            let panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
}