
export function init() {
    let languageList = document.getElementById("language-select");
    let transcriptList = document.getElementById("active-transcript");
    let transcripts = transcriptList.children;
    transcripts[0].style.display = "block";
    
    if (!languageList) {
        // If the language list was not built into this page (i.e. there was only one transcript to display), 
        // then don't set up event listeners for the language list
        return;
    }
    
    languageList.selectedIndex = 0;
    languageList.addEventListener("click", function() {
        for (let i = 0; i < transcripts.length; i++) {
            transcripts[i].style.display = i === languageList.selectedIndex ? "block" : null;
        }
    })
}
