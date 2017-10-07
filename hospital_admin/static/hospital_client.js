/**** START CONSTANTS****/
//True or False
var DEBUG = true,
    APP_URL = "http://localhost:5000/hospital/api",
//Either json or xml can be selected as  response format. 
    RESPONSE_FORMAT = "json",
//Format of the request
    CONTENT_TYPE = "application/" + RESPONSE_FORMAT,

    DEFAULT_USER = "",
    DEFAULT_PASSWORD = "";
/**** END CONSTANTS****/

/**** START RESTFUL CLIENT****/

function get_nurses_list() {
    //http://localhost:5000/forum/api/nurses
    var arr = [APP_URL, "nurses"];
    var apiurl = arr.join("/");
    return $.ajax({
        url: apiurl,
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": DEFAULT_PASSWORD}
    }).always(function () {
        //Remove old list of nurses, clear the form data hide the content information(no selected)
        $("#nurse_list").empty();
        clearNurseInfo();
        $("#mainContent").hide();

    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }

        if (RESPONSE_FORMAT === "json") {
            nurses = data['nurses_list']
            for (var i = 0; i < nurses.length; i++) {
                var nurse = nurses[i];
                //alert(nurse.name);
                appendNurseToList(nurse.link.href, nurse.nurse_id, nurse.name);
            }
        }

        else if (RESPONSE_FORMAT === "xml") {

        }

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        //Inform nurse about the error using an alert message.
        alert("Could not fetch the list of nurses.  Please, try again");

    });
}


function getNurse(apiurl) {
    return $.ajax({
        url: apiurl,
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": "admin"}
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        $("#nurse_form").attr('action', apiurl);

        if (RESPONSE_FORMAT === "json") {
            var nurse = data.nurse;
            $("#nurse_profile").attr('action', apiurl);
            var nurse_patients_list_url = nurse.link.href;
            $("#name").val(nurse.name);
            $("#surname").val(nurse.surname);
            $("#phone_number").val(nurse['phone number']);
            $("#address").val(nurse.address);
            $.when(
                getNursePatientsList(nurse_patients_list_url, apiurl)
            )
                .always(function () {
                    $("#newNurseData").hide();
                    $("#newMedicamentData").hide();
                    $("#existingNurseData").show();
                    //Be sure that the content is shown
                    $("#mainContent").show();
                });
        }

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Cannot extract information about this nurse from the hospital service.");
        $("#nurse_list li.selected").removeClass("selected");
        $("#mainContent").hide();
    });
}


function getNursePatientsList(apiurl, nurseurl) {
    return $.ajax({
        url: apiurl,
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": "admin"}
    }).always(function () {
        $("#nurse").empty();

    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        $("#patientsNumber").text(data.nurses_patient_list.length);
        if (RESPONSE_FORMAT === "json") {
            pats = data['nurses_patient_list'];
            for (var i = 0; i < pats.length; i++) {
                getPatient(pats[i].link.href, nurseurl);
            }
        }

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Could not fetch the nurse's patients list.  Please, try again");

    });
}


function addNurse(apiurl, nurseData) {
    return $.ajax({
        url: apiurl,
        type: "POST",
        data: nurseData,
        processData: false,
        contentType: CONTENT_TYPE,
        headers: {"Authorization": "admin"}
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        alert("Nurse successfully added");
        $nurse = appendNurseToList(jqXHR.getResponseHeader("Location"));
        $nurse.click();

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Could not create new nurse");
    });
}


function editNurseProfile(apiurl, profile) {
    return $.ajax({
        url: apiurl,
        type: "PUT",
        data: profile,
        processData: false,
        contentType: CONTENT_TYPE,
        headers: {"Authorization": "admin"}
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        alert("Nurse's profile successfully edited");

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        var error_message = $.parseJSON(jqXHR.responseText).message
        alert("Could not edit the nurse's profile");
        reloadNurseData();
    });
}


function deleteNurse(apiurl) {
    $.ajax({
        url: apiurl,
        type: "DELETE",
        headers: {"Authorization": "admin"},
        dataType: RESPONSE_FORMAT
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        alert("The nurse has been deleted from the database");
        //Update the list of nurses from the server.
        get_nurses_list();

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("The nurse could not be deleted from the database");
    });
}

/*

New Addition on October 7 2017.

*/
function get_patients_list() {
    //http://localhost:5000/forum/api/nurses
    var arr = [APP_URL, "nurses"];
    var apiurl = arr.join("/");
    return $.ajax({
        url: apiurl,
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": DEFAULT_PASSWORD}
    }).always(function () {
        //Remove old list of nurses, clear the form data hide the content information(no selected)
        $("#nurse_list").empty();
        clearNurseInfo();
        $("#mainContent").hide();

    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }

        if (RESPONSE_FORMAT === "json") {
            nurses = data['nurses_list']
            for (var i = 0; i < nurses.length; i++) {
                var nurse = nurses[i];
                //alert(nurse.name);
                appendNurseToList(nurse.link.href, nurse.nurse_id, nurse.name);
            }
        }

        else if (RESPONSE_FORMAT === "xml") {

        }

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        //Inform nurse about the error using an alert message.
        alert("Could not fetch the list of nurses.  Please, try again");

    });
}
/*

End. New Addition on October 7 2017.
Checking github.s

*/

function getPatient(apiurl, nurseurl) {
    $.ajax({
        url: apiurl,
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": "admin"}
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        var patient = data.patient;
        var name = patient.name;
        var surname = patient.surname;
        var room = patient.room;
        var medication = patient.link.href;
        appendPatientToList(apiurl, name, surname, room, medication, nurseurl);
        getMedication(medication, name, surname, room, apiurl, nurseurl);

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Cannot get information from patient: " + apiurl);
    });
}


function deletePatient(apiurl) {
    $.ajax({
        url: apiurl,
        type: "DELETE",
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": "admin"}
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        alert("The patient was deleted successfully");
        reloadNurseData();

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Could not delete the patient");
    });
}


function getMedication(apiurl, pname, psurname, proom, purl, nurl) {
    return $.ajax({
        url: apiurl,
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": "admin"}
    }).always(function () {
        $("#patient_medication_list").empty();

    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        $("#medicationNumber").text(data.patient_medication_list.length);
        if (RESPONSE_FORMAT === "json") {
            meds = data['patient_medication_list'];
            for (var i = 0; i < meds.length; i++) {
                getMedicament(meds[i].link.href, pname, psurname, proom, purl, nurl);
            }
        }

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Could not fetch the patient medication list.  Please, try again");
    });
}


function getMedicament(apiurl, pname, psurname, proom, purl, nurl) {
    $.ajax({
        url: apiurl,
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": "admin"}
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        var medicament = data.medicament;
        var name = medicament.name;
        var dosage = medicament.dosage;
        var duration = medicament.duration;
        var hours = medicament.hours;
        var bag_volume = medicament['bag volume'];
        var administration = medicament.administration;
        appendMedicamentToList(apiurl, name, dosage, duration, hours, bag_volume, administration, pname, psurname, proom, purl, nurl);

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Cannot get information from medicament: " + apiurl);
    });
}


function addMedicament(apiurl, medicamentData) {
    return $.ajax({
        url: apiurl,
        type: "POST",
        data: medicamentData,
        processData: false,
        headers: {"Authorization": "admin"},
        contentType: CONTENT_TYPE
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        alert("Medicament successfully added");
        $medicament = appendMedicamentToList(jqXHR.getResponseHeader("Location"));
        $medicament.click();

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Could not create new medicament");
    });
}


function deleteMedicament(apiurl) {
    $.ajax({
        url: apiurl,
        type: "DELETE",
        dataType: RESPONSE_FORMAT,
        headers: {"Authorization": "admin"}
    }).done(function (data, textStatus, jqXHR) {
        if (DEBUG) {
            console.log("RECEIVED RESPONSE: data:", data, "; textStatus:", textStatus)
        }
        alert("The medicament was deleted successfully");
        reloadNurseData();

    }).fail(function (jqXHR, textStatus, errorThrown) {
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown)
        }
        alert("Could not delete the medicament");
    });
}


/**** END RESTFUL CLIENT****/


/**** BUTTON HANDLERS ****/


/******** To remove ***/


function handleGetNurse2(event) {
    if (DEBUG) {
        console.log("Triggered handleEditNurse")
    }
    var $form = $(this).closest("form");
    var nurseurl = $form.attr("action");
    alert("edit nurse falso")
    //Extract the values from the form and store it in a Object literal.
    var nurse = {};
    var name = $form.find("#name").val();
    var surname = $form.find("#surname").val();
    var phone_number = $form.find("#phone_number").val();
    var address = $form.find("#address").val();

    if (name)
        nurse.name = name;
    if (surname)
        nurse.surname = surname;
    if (phone_number)
        nurse.phone_number = phone_number;
    if (address)
        nurse.address = address

    editNurseProfile(nurseurl, JSON.stringify(nurse));
}

/****       *****/


function handleGetNurse(event) {
    if (DEBUG) {
        console.log("Triggered handleGetNurse")
    }
    //Clean old content from previous nurse
    clearNurseInfo();
    //Hide newNurseData an show existingNurseData
    //alert("Adios")
    $("#newNurseData").hide();
    $("#newMedicamentData").hide();
    $("#existingNurseData").show();
    //Deselect any previous nurse from the nurse list.
    $("#nurse_list .selected").removeClass("selected");
    $(this).addClass("selected");
    var url = $(this).children("a").attr("href");
    getNurse(url);
    return false;
}


function handleAddNurse(event) {
    if (DEBUG) {
        console.log("Triggered handleAddNurse")
    }
    $("#nurse_list li").removeClass("selected");
    clearNewNurseInfo();
    $("#existingNurseData").hide();
    $("#newMedicamentData").hide();
    $("#newNurseData").show();
    $("#mainContent").show();
}


function handleCreateNurse(event) {
    if (DEBUG) {
        console.log("Triggered handleCreateNurse")
    }
    var $form = $(this).closest("form");
    //var id = $form.find("#new_id").val(); Obtener new_id para crear nueva enfermera (ver append_nurse en database.py linea 215)
    var arr = [APP_URL, "nurses", ''];
    var nursesurl = arr.join("/");

    //Extract the values from the form and store it in a Object literal.
    var nurse = {};
    var name = $form.find("#new_name").val();
    var surname = $form.find("#new_surname").val();
    var phone_number = $form.find("#new_phone_number").val();
    var address = $form.find("#new_address").val();
    //If the fields are empty do not add the value to the nurse_profile
    if (name)
        nurse.name = name;
    if (surname)
        nurse.surname = surname;
    if (phone_number)
        nurse.phone_number = phone_number;
    if (address)
        nurse.address = address;
    //var nurse = {"nurse":nurse}
    addNurse(nursesurl, JSON.stringify(nurse));
}


function handleEditNurse(event) {
    if (DEBUG) {
        console.log("Triggered handleEditNurse")
    }
    var $form = $(this).closest("form");
    var nurseurl = $form.attr("action");

    alert("edit nurse verdadero")

    //Extract the values from the form and store it in a Object literal.
    var nurse = {};
    var name = $form.find("#name").val();
    var surname = $form.find("#surname").val();
    var phone_number = $form.find("#phone_number").val();
    var address = $form.find("#address").val();

    if (name)
        nurse.name = name;
    if (surname)
        nurse.surname = surname;
    if (phone_number)
        nurse.phone_number = phone_number;
    if (address)
        nurse.address = address

    editNurseProfile(nurseurl, JSON.stringify(nurse));
}


function handleDeleteNurse(event) {
    //Extract the url of the resource from the form action attribute.
    if (DEBUG) {
        console.log("Triggered handleDeleteNurse")
    }

    var nurseurl = $(this).closest("form").attr("action");
    deleteNurse(nurseurl);
}


function handleDeletePatient(event) {
    if (DEBUG) {
        console.log("Triggered handleDeletePatient")
    }

    var patienturl = $(this).closest("form").attr("action");
    deletePatient(patienturl);
}


function handleAddMedicament(event) {
    if (DEBUG) {
        console.log("Triggered handleAddMedicament")
    }
    $("#medicaments list2").removeClass("selected");
    clearNewMedicamentInfo();
    $("#existingNurseData").hide();
    $("#newNurseData").hide();
    $("#newMedicamentData").show();
    $("#mainContent").show();
}


function handleCreateMedicament(event) {
    if (DEBUG) {
        console.log("Triggered handleCreateMedicament")
    }
    var $form = $(this).closest("form");
    //var id = $form.find("#new_id").val(); Obtener new_id para crear nueva enfermera (ver append_nurse en database.py linea 215)
    var arr = [APP_URL, "nurses", "nur-0", "patients", "pat-1", "medication", ''];
    var medicationurl = arr.join("/");

    //Extract the values from the form and store it in a Object literal.
    var medication = {};
    var name = $form.find("#new_name").val();
    var dosage = $form.find("#new_dosage").val();
    var duration = $form.find("#new_duration").val();
    var hours = $form.find("#new_hours").val();
    var bag_volume = $form.find("#new_bag_volume").val();
    var administration = $form.find("#new_administration").val();

    if (name)
        medication.name = name;
    if (dosage)
        medication.dosage = dosage;
    if (duration)
        medication.duration = duration;
    if (hours)
        medication.hours = hours;
    if (bag_volume)
        medication.bag_volume = bag_volume;
    if (administration)
        medication.administration = administration;

    addMedicament(medicationurl, JSON.stringify(medication));
}


function handleDeleteMedicament(event) {
    if (DEBUG) {
        console.log("Triggered handleDeleteMedicament")
    }

    var medicamenturl = $(this).closest("form").attr("action");
    deleteMedicament(medicamenturl);
}


/**** END BUTTON HANDLERS ****/

/**** UI HELPERS ****/

function appendNurseToList(url, id, name) {
    if (!id) {
        id = url.substring(url.lastIndexOf("/", url.length - 2) + 1, url.length - 1);
    }
    var $nurse = $('<li>').html('<a href="' + url + '">' + name + '</a>');
    //var $nurse = $('<li>').html('<a href="'+url+'">'+id+'</a>');

    //Add to the nurse list
    $("#nurse_list").append($nurse);
    return $nurse;
}


function appendPatientToList(apiurl, name, surname, room, url, nurseurl) {
    var $patient = $("<div>").addClass('patient').html("" +
        "<form action='" + apiurl + "'>" +
        "<header class='patientIntro'>" +
        "<span class='patientName'>" + name + " " + surname + "</span>" +
        "</header>" +
        "<p class='patientRoom'>Patient room: " + room + "</p>" +
        "<p class='patientMedication'>Patient medication list: <a href='" + url + "'>Medication</a></p>" +

        "<input id='nurse_profile2' type='button' value='Nurse Profile'/>" +
            //"<p class='patientNurse'>Patient's nurse profile: <a href='http://www.google.com'>Nurse Profile</a></p>"+

            //"<p class='patientNurse'>Patient's nurse profile: <a href='"+nurseurl+"'>Nurse Profile</a></p>"+
        "<div class='patientTools' >" +
        "<span class='commands'><input id='deletePatient' type='button' value='Delete'/></span>" +
        "</div>" +
        "</form>"
    );
    $("#patients #list").append($patient);
}


function appendMedicamentToList(apiurl, name, dosage, duration, hours, bag_volume, administration, pname, psurname, proom, purl, nurl) {
    var $medicament = $("<div>").addClass('medicament').html("" +
        "<form action='" + apiurl + "'>" +
        "<header class='medicamentIntro'>" +
        "<span class='medicamentName'>" + name + " (room " + proom + ")</span>" +
        "</header>" +
        "<p class='medicamentPrescription'>" + dosage + " during " + duration + " " + hours + "</p>" +
        "<p class='medicamentBagVolume'>" + bag_volume + " via " + administration + "</p>" +
        "<p class='medicamentPatient'>Related patient: <a href='" + purl + "'>" + pname + " " + psurname + "</a></p>" +
        "<p class='medicamentNurse'>Related nurse: <a href='" + nurl + "'>Nurse Profile</a></p>" +
        "<div class='medicamentTools' >" +
        "<span class='commands'><input id='deleteMedicament' type='button' value='Delete'/></span>" +
        "</div>" +
        "</form>"
    );
    $("#medicaments #list2").append($medicament);
}


function clearNurseInfo() {
    //Remove resource from the form
    $("form#nurse_profile").attr('action', '#');
    //Remove the values from all inputs in the form
    $("form#nurse_profile").get(0).reset();
    //Reset the number of patients
    $("#patientNumber").text("");
    //Clean the patient list
    $("#patients #list").empty();
    //Reset the number of medicaments
    $("#medicamentNumber").text("");
    //Clean the medicament list
    $("#medicaments #list2").empty();
}


function clearNewNurseInfo() {
    //Remove resource from the form
    $("form#create_nurse_form").attr('action', '#');
    //Remove the values from all inputs in the form
    $("form#create_nurse_form").get(0).reset();
}


function clearNewMedicamentInfo() {
    //Remove resource from the form
    $("form#create_medicament_form").attr('action', '#');
    //Remove the values from all inputs in the form
    $("form#create_medicament_form").get(0).reset();
}


function reloadNurseData() {
    var nurseurl = $("form#nurse_form").attr('action');
    clearNurseInfo();
    getNurse(nurseurl);
}


/*** END UI HELPERS***/

/*** START ON LOAD ***/
//This method is executed when the webpage is loaded.
$(function () {

    $("#saveNurse").on("click", handleEditNurse);
    $("#deleteNurse").on("click", handleDeleteNurse);
    $("#addNurse").on("click", handleAddNurse);
    $("#createNurse").on("click", handleCreateNurse);

    $("#list").on("click", "#deletePatient", handleDeletePatient);
    $("#nurse_list").on("click", "li", handleGetNurse);

    $("#nurse_profile2").on("click", handleEditNurse);
    //$("#list_profile").on("click", "#nurse_profile2", handleGetNurse);
    //$("#list_profile").on("click", "#nurse_profile2", handleGetNurse2);

    $("#list2").on("click", "#deleteMedicament", handleDeleteMedicament);
    $("#list2").on("click", "#addMedicament", handleAddMedicament);
    $("#createMedicament").on("click", handleCreateMedicament);

    get_nurses_list();
    get_patients_list();
});
/*** END ON LOAD**/