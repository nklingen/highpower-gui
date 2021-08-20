// spawn_python.js


function runPython() {
    //document.getElementById("p1").innerHTML = "New text!"+Math.random();

    mv_cabinet1 = window.localStorage.getItem("C1mV");
    mv_cabinet2 = window.localStorage.getItem("C2mV");
    mv_cabinet3 = window.localStorage.getItem("C3mV");
    mv_cabinet4 = window.localStorage.getItem("C4mV");
    document.getElementById("p1").innerHTML = mv_cabinet1;

    

    const PID = window.electron.runPython(mv_cabinet1, mv_cabinet2,mv_cabinet3,mv_cabinet4).return;
    
    window.localStorage.setItem("PID", PID);
    document.getElementById("p1").innerHTML = "Oline hej";
    //document.getElementById("p1").innerHTML = PID;

    


}

function killPython() {
    const PID = window.localStorage.getItem("PID");
    window.electron.killPython(PID);
    //document.getElementById("p1").innerHTML = "killed";
}
