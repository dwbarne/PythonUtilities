
//Copyright (c) 2000-2003 Microsoft Corporation. All rights reserved.
var iSelectedIndex = -1;var fDHTMLEnabled = false;var fRemove = false;
function EditDN()
{if (iSelectedIndex != -1)
document.AnrFormData.AddressSelect[iSelectedIndex].checked = false;}

function EditEmail()
{document.MainForm.EmailAddress.value = document.MainForm.EmailAddressDisplay.value;if (iSelectedIndex != -1)
document.AnrFormData.AddressSelect[iSelectedIndex].checked = false;}

function InitEditRecip()
{if(document.MainForm.EmailAddressDisplay.value == "")
{if (document.MainForm.EmailAddress.value.indexOf("MAPIPDL:") == 0)
document.MainForm.EmailAddressDisplay.value = document.MainForm.DisplayName.value;else
document.MainForm.EmailAddressDisplay.value = document.MainForm.EmailAddress.value;}
}

function WarnUser(level, url)
{var fOpen = true;if (level == 1)
fOpen = confirm(L_WarnUnsafe);if (fOpen)
{window.open(g_szURL + url);}
return(false);}

function OnLoad()
{if(document != null && document.MainForm != null && document.MainForm.FolderName != null)
{document.MainForm.FolderName.focus();}
if (document.all)
{var verRegExp=/MSIE \d+.\d+/;var oVer = navigator.appVersion.match(verRegExp);if (oVer == null)
return;var verIExp=/ \d+.\d+/;oVer = oVer[0].match(verIExp);if (oVer == null)
return;if (5 <= parseInt(oVer[0], 10))
fDHTMLEnabled = true;}
}

function SetAction(actionValue)
{document.MainForm.Action.value = actionValue;document.MainForm.submit();}

function SubmitGALFind()
{if (document.galfind.DN.value == "" && document.galfind.FN.value == "" &&
document.galfind.LN.value == "" && document.galfind.TL.value == "" &&
document.galfind.AN.value == "" && document.galfind.CP.value == "" &&
document.galfind.DP.value == "" && document.galfind.OF.value == "" &&
document.galfind.CY.value == "")
{alert(g_szNoSearchInfo);document.galfind.DN.focus();}
else
document.galfind.submit();}

function NameSelect_OnClick(index)
{iSelectedIndex = index;if (typeof document.AnrFormData.AnrName.length != "undefined")
{document.MainForm.DisplayName.value = document.AnrFormData.AnrName[index].value;document.MainForm.EmailAddress.value = document.AnrFormData.AnrAddress[index].value;if (document.AnrFormData.AnrAddress[index].value.indexOf("MAPIPDL:") == 0)
document.MainForm.EmailAddressDisplay.value = document.AnrFormData.AnrName[index].value;else
document.MainForm.EmailAddressDisplay.value = document.AnrFormData.AnrAddress[index].value;}
else
{document.MainForm.DisplayName.value = document.AnrFormData.AnrName.value;document.MainForm.EmailAddress.value = document.AnrFormData.AnrAddress.value;if (document.AnrFormData.AnrAddress.value.indexOf("MAPIPDL:") == 0)
document.MainForm.EmailAddressDisplay.value = document.AnrFormData.AnrName.value;else
document.MainForm.EmailAddressDisplay.value = document.AnrFormData.AnrAddress.value;}
if (fRemove)
{fRemove = false;document.MainForm.RecipientType[document.AnrFormData.DefaultType.value - 1].checked = true;}
}

function RemoveRecip_OnClick()
{if(-1 != iSelectedIndex)
{document.AnrFormData.AddressSelect[iSelectedIndex].checked = false;document.MainForm.DisplayName.value = document.OrigRecipForm.DisplayName.value;document.MainForm.EmailAddressDisplay.value = "";document.MainForm.EmailAddress.value = "";iSelectedIndex = -1;}
fRemove = true;}

function OnCmd_Click(type)
{if ((fRemove && document.MainForm.isCDLEdit !=null && (document.MainForm.isCDLEdit.value=="1")) || type == 1)
{document.MainForm.Action.value = "Cancel";SetCmd(cmdSaveRecipient);}
else if(type == 0)
{document.MainForm.Action.value = "Apply";SetCmd(cmdSaveRecipient);}
else if(type == 1)
{document.MainForm.Action.value = "Cancel";SetCmd(cmdSaveRecipient);}
}

function StartCompose_EditRecip()
{if (document && document.MainForm && document.AnrFormData.DefaultType)
{document.MainForm.RecipientType[document.AnrFormData.DefaultType.value - 1].checked = true;}
}

function SubmitRemoveForm(cmdVal)
{document.removeForm.Cmd.value = cmdVal;document.removeForm.submit();}

function showCalendar()
{var iM = Number(g_dtPatternStart.substring(5,7))-1;var iMs=Date.UTC(g_dtPatternStart.substring(0,4),iM,g_dtPatternStart.substring(8,10),g_dtPatternStart.substring(11,13),g_dtPatternStart.substring(14,16),0,0)
var oD=new Date(iMs);var iFullYear = oD.getYear();if (iFullYear < 1000) 
iFullYear += (iFullYear>69)?1900:2000;window.open(g_sCalendar+"/?cmd=contents&m="+(oD.getMonth()+1)+"&d="+oD.getDate()+"&y="+iFullYear+"&view=daily","","toolbar=0,location=0,directories=0,status=1,menubar=0,scrollbars=1,resizable=1,width=800,height=480");}

function ModCheckBox(obj)
{var oCheckBoxes = window.document.galfind.MsgID;if (oCheckBoxes != null && oCheckBoxes.length != null && obj.checked && document.galfind.US != null && document.galfind.US.value == "C")
{for (var i = 0;i < oCheckBoxes.length;i++)
{if (oCheckBoxes[i] != obj)
oCheckBoxes[i].checked = false;SetCheckBoxRow(oCheckBoxes[i]);}
}
else
{SetCheckBoxRow(obj);}
}

function SetCheckBoxRow(obj)
{if (fDHTMLEnabled && obj && obj.tagName)
{var oItm = obj;while (oItm.tagName!="TR")
{oItm=oItm.parentNode;}
if (obj.checked)
oItm.className = "vwSelItm";else
oItm.className = "";}
}

function UpdateParent(iType)
{if (document.galfind.US != null & window.opener != null && window.document.galfind.MsgID)
{var oField = null;var oOpenerForm = window.opener.document.MainForm;switch (iType)
{case 1:
if (document.galfind.US.value == "M" || document.galfind.US.value == "F")
oField = oOpenerForm.MsgTo;else if (document.galfind.US.value == "A")
oField = oOpenerForm.Required;else if (document.galfind.US.value == "C")
oField = oOpenerForm.member;break;case 2:
if (document.galfind.US.value == "M")
oField = oOpenerForm.MsgCc;else if (document.galfind.US.value == "A")
oField = oOpenerForm.Optional;break;case 3:
if (document.galfind.US.value == "M")
oField = oOpenerForm.MsgBcc;else if (document.galfind.US.value == "A")
oField = oOpenerForm.Resource;break;}
if (oField != null)
{if (oOpenerForm.DATACHANGED != null)
oOpenerForm.DATACHANGED.value ="1";var oCheckBoxes = window.document.galfind.MsgID;if (oCheckBoxes.length == null && oCheckBoxes.checked)
{if (document.galfind.US.value == "C") 
oField.value = "";else
AddSemiColon(oField);oCheckBoxes.checked = false;SetCheckBoxRow(oCheckBoxes);oField.value += oCheckBoxes.value;if (document.galfind.US.value == "C" && !oOpenerForm.addButton.disabled) 
oOpenerForm.addButton.click();}
else
{var fFirstAddition = true;for (var i = 0;i < oCheckBoxes.length;i++)
{if (oCheckBoxes[i].checked)
{if (document.galfind.US.value == "C") 
oField.value = "";if (fFirstAddition)
{fFirstAddition=false;AddSemiColon(oField);}
else
{oField.value += "; ";}
oCheckBoxes[i].checked = false;SetCheckBoxRow(oCheckBoxes[i]);oField.value += oCheckBoxes[i].value;if (document.galfind.US.value == "C" && !oOpenerForm.addButton.disabled) 
oOpenerForm.addButton.click();}
}
}
}
}
}

function AddSemiColon(oField)
{if (oField.value.length > 0)
{var i = oField.value.length - 1;while (i >= 0 && oField.value.charAt(i) == " ")
{i--;}
if (i >= 0)
{if (oField.value.charAt(i) == ";")
oField.value = oField.value.substring(0,i);else
oField.value = oField.value.substring(0,i+1);oField.value += "; ";}
else
{oField.value = "";}
}
}
