function showPopup() {
	document.getElementById('pop-up').className = 'visible';
}

function hidePopup() {
	document.getElementById('pop-up').className = 'hidden';
}

function kaikuConfirm(confirmationText) {
	return confirm(confirmationText);
}

function checkOtherEnter(e,usebutton) {
	var keyCode;
	if(window.event){
		keyCode = window.event.keyCode;
	}else if(e){
		keyCode = e.which;
	}
	if (keyCode == 13 && usebutton) {
		document.getElementById(usebutton).click();
	}
}

function noEnter(e) {
	var keyCode;
	if(window.event){
		keyCode = window.event.keyCode;
	}else if(e){
		keyCode = e.which;
	}
	if (keyCode == 13 ) {
		//void(0);
		return false;
	}
}


/*
 * Show div
 */
function showDiv(divId) {
	var divElement = document.getElementById(divId);
	if (divElement) {
		divElement.style.display = 'block';
	}
}

/*
 * Hide div 
 */
function hideDiv(divId) {
	var divElement = document.getElementById(divId);
	if (divElement) {
		divElement.style.display = 'none';
	}
}

/*
 * Show or Hide div 
 */
function showHideDiv(divId) {
	var divElement = document.getElementById(divId);
	if (divElement) {
		if(divElement.style.display == 'none'){
			divElement.style.display = 'block';
		}else{
			divElement.style.display = 'none';
		}
	}
}


/* responsible management -->*/

function setModifiedCourseGroupId(useValue) {
	var obj = document.getElementById("modifiedCourseGroupId");
	if (obj) {
		obj.value = useValue;
	}
}

function setSelectedUsr(useValue) {
	var obj = document.getElementById("selectedUsr");
	if (obj) {
		obj.value = useValue;
	}
}

function deleteResponsibleConfirm(usr,msg) {

if(kaikuConfirm(msg)){
	setSelectedUsr(usr);
	return true;
}
return false;
}
/* <-- responsible management */

/* moving options across two option lists -->*/

function addOption(theSel, theText, theValue)
{

  var newOpt = new Option(theText, theValue);
  var selLength = theSel.length;
  theSel.options[selLength] = newOpt;
}

function deleteOption(theSel, theIndex)
{ 
  var selLength = theSel.length;
  if(selLength>0)
  {
    theSel.options[theIndex] = null;
  }
}

function moveOptions(theSelFrom, theSelTo)
{
  
  var selLength = theSelFrom.length;
  var selectedText = new Array();
  var selectedValues = new Array();
  var selectedCount = 0;
  
  var i;
  
  // Find the selected Options in reverse order
  // and delete them from the 'from' Select.
  for(i=selLength-1; i>=0; i--)
  {
    if(theSelFrom.options[i].selected && !theSelFrom.options[i].disabled)
    {
      selectedText[selectedCount] = theSelFrom.options[i].text;
      selectedValues[selectedCount] = theSelFrom.options[i].value;
      deleteOption(theSelFrom, i);
      selectedCount++;
    }
  }
  
  // Add the selected text/values in reverse order.
  // This will add the Options to the 'to' Select
  // in the same order as they were in the 'from' Select.
  for(i=selectedCount-1; i>=0; i--)
  {
    addOption(theSelTo, selectedText[i], selectedValues[i]);
  }
  
  sortlist(theSelTo);

}

function sortlist(selElem) {                 
	var tmpAry = new Array();                 
	for (var i=0;i<selElem.options.length;i++) {                         
		tmpAry[i] = new Array();                         
		tmpAry[i][0] = selElem.options[i].text;                         
		tmpAry[i][1] = selElem.options[i].value; 
		tmpAry[i][2] = selElem.options[i].disabled; 
		if(selElem.options[i].style != null){
			tmpAry[i][3] = selElem.options[i].style.color; 
		}
	}                 
	tmpAry.sort();                 
	while (selElem.options.length > 0) {                     
		selElem.options[0] = null;                 
	}                 
	for (var i=0;i<tmpAry.length;i++) {                         
		var op = new Option(tmpAry[i][0], tmpAry[i][1]);  
		op.disabled = tmpAry[i][2];
		
		if(tmpAry[i][3] != null){
			op.style.color = tmpAry[i][3];
		}
		selElem.options[i] = op;  
	}                 
	return;
}

function setAllSelected(theSel){
	for(var i=0; i < theSel.options.length; i++){
		theSel.options[i].selected=true;
	}
}


function showCorrectDepartmentList() {
	var list = document.getElementById("chosenAcademicYear");
	var year = list.options[list.selectedIndex].value;
	if(year >= 2013) {
		document.getElementById("oldChosenDepartment").style.display = "none";
		document.getElementById("chosenDepartment").style.display = "inline"
	}
	else {
		document.getElementById("oldChosenDepartment").style.display = "inline";
		document.getElementById("chosenDepartment").style.display = "none"
	}
}


$(function() {
	
	/* footer info pop-up */
	var boxWidth = 250;
	var boxHeight = 100;
	var d = $('#footerInfobox').dialog({
		autoOpen: false,
		width: boxWidth,
		height: boxHeight,
		position: {my: "right bottom", at: "right top", of: "#footer"}
	});
	/* opening */
	$('#footerInfoLink').click(function() {
		d.dialog('open'); 
	});
	
	$('#reportsSubmit').click(function() {
		$('#reportMessages').empty(); 
	});
});

//Count and limit feedback summary response length
$(function() {
	var maximumCharacterCount = 4000;
	
	var responseLength = $('#feedbackResultsResponse').val().length;
	var charactersRemaining = maximumCharacterCount - responseLength;
	$('#feedbackResultsResponseCharCount').val(charactersRemaining < 0 ? 0 : charactersRemaining);
	
	$('#feedbackResultsResponse').keyup(function() {
		var responseLength = $('#feedbackResultsResponse').val().length;
		if(responseLength > maximumCharacterCount) {
			$('#feedbackResultsResponse').val($('#feedbackResultsResponse').val().substring(0, responseLength - 1));
		}
		
		var charactersRemaining = maximumCharacterCount - responseLength;
		$('#feedbackResultsResponseCharCount').val(charactersRemaining < 0 ? 0 : charactersRemaining);
	});
});




