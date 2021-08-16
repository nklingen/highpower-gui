// spawn_python.js


function runPython() {
    document.getElementById("p1").innerHTML = "New text!"+Math.random();

    watts_cabinet1 = window.localStorage.getItem("C1watts");

    watts_cabinet2 = window.localStorage.getItem("C2watts");
    watts_cabinet3 = window.localStorage.getItem("C3watts");
    watts_cabinet4 = window.localStorage.getItem("C4watts");

    thread_cabinet1 = window.localStorage.getItem("C1thread");
    thread_cabinet2 = window.localStorage.getItem("C2thread");
    thread_cabinet3 = window.localStorage.getItem("C3thread");
    thread_cabinet4 = window.localStorage.getItem("C4thread");
    

    const PID = window.electron.runPython([watts_cabinet1, thread_cabinet1,watts_cabinet2, thread_cabinet3,watts_cabinet3, thread_cabinet3,watts_cabinet4, thread_cabinet4]).return;
    
    window.localStorage.setItem("PID", PID);
    document.getElementById("p1").innerHTML = "Oline hej";
    document.getElementById("p1").innerHTML = PID;

    


}

function killPython() {
    const PID = window.localStorage.getItem("PID");
    window.electron.killPython(PID);
    document.getElementById("p1").innerHTML = "killed";
}

function getInformation() {

    
    document.getElementById("p1").innerHTML = "hello";
    const info = window.electron.getInformation(1).return;
    document.getElementById("p1").innerHTML = "hi";
    document.getElementById("p1").innerHTML = info;
    



}
