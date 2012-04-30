
//Copyright (c) 2000-2003 Microsoft Corporation. All rights reserved.
var cmdSend	= "send";var cmdSendCancel	= "sendcancel";var cmdSubmitPost	= "submitpost";var cmdSave	= "save";var cmdMove	= "moveselect";var cmdCopy	= "copyselect";var cmdSaveAppt	= "saveappt";var cmdSendAppt	= "sendappt";var cmdDelete	= "delete";var cmdEditRecip	= "editrecipient";var cmdEditAttach	= "editattach";var cmdCheckNames	= "checknames";var cmdSaveRecipient	= "saverecipient";var cmdResolveFB	= "resolvefb";var cmdEditRecurrence	= "editrecurrence";var cmdOptions	= "options";var cmdMailTo	= "mailtouri";var cmdNYI	= "nyi";var cmdTaskDetails	= "taskdetails";var cmdSaveTask	= "savetask";var cmdSaveTaskDetails	= "savetaskdetails";var cmdTaskRecurrence	= "taskrecurrence";var cmdSaveTaskRecurrence	= "savetaskrecurrence";var objDeliveryReceiptField	= null;var objReadReceiptField	= null;
function forceSave()
{alert(L_SaveAttToDsk);return false;}

function NavigateTo(loc)
{this.location = loc;}

function CheckWork (oField)
{if (oField != -1)
{var lMins = oField.value;if (lMins > g_lWrkMaxMin)
{alert (g_szMaxDuration);return false;}
}
return true;}

function CheckTaskWork()
{return (CheckWork(g_ofEstWork) && CheckWork(g_ofActWork));}

function SetCmd(cmd)
{if (cmd == cmdEditAttach && typeof g_fAllowAttachments != "undefined" && !g_fAllowAttachments)
{alert(g_szAttachmentsNotAllowed);return;}
if (cmd == cmdSaveTaskDetails)
{if (!CheckTaskWork()) return;}
if (typeof g_fIsContactDLItem != "undefined" && true == g_fIsContactDLItem)
{if (cmdSave == cmd && "" == document.MainForm[0].value && !confirm(g_szCDL_NoName_Text))
{return;}
}
document.MainForm.Cmd.value = cmd;if (typeof CustomSubmit != "undefined")
CustomSubmit();document.MainForm.submit();}

function EditRecip(index)
{document.MainForm.Cmd.value = cmdEditRecip;document.MainForm.Index.value = index;if (typeof CustomSubmit != "undefined")
CustomSubmit();document.MainForm.submit();}

function StartCompose()
{if (typeof g_fIsContactItem == "undefined" || false == g_fIsContactItem)
{var bReply = (window.location.search.indexOf("Cmd=reply") != -1);var bSignatureCase = (typeof g_bAutoSignatureOn != "undefined" && true == g_bAutoSignatureOn);var oBody = null;if (bReply || bSignatureCase)
{var	i;var	composeForm = document.MainForm;for(i =	0;composeForm[i] != null;i++)
{if(composeForm[i].name == "urn:schemas:httpmail:textdescription")
{oBody = composeForm[i];break;}
}
}
if (bSignatureCase)
{if (oBody != null)
{oBody.value = "\r\n\r\n" + oBody.value;}
}
if(!bReply)
{if(document	&& document.MainForm && document.MainForm.MsgTo)
{document.MainForm.MsgTo.focus();}
}
else
{if (oBody != null)
{oBody.focus();}
}
}
if (typeof g_fIsEnableReceipts != "undefined")
{InitReceiptSelection();}
if (typeof g_fIsContactItem != "undefined" && true == g_fIsContactItem)
{StartCompose_Contact();}
if (typeof CustomOnload != "undefined")
CustomOnload();if (typeof g_fIsEditRecipForm != "undefined" && true == g_fIsEditRecipForm)
StartCompose_EditRecip();}

function InitReceiptSelection()
{var composeForm = document.MainForm;var i;for(i = 0;composeForm[i] != null;i++)
{if(composeForm[i].name == "http://schemas.microsoft.com/exchange/deliveryreportrequested")
{objDeliveryReceiptField = composeForm[i];}
if(composeForm[i].name == "http://schemas.microsoft.com/exchange/readreceiptrequested")
{objReadReceiptField = composeForm[i];}
}
var index = 0;if (objDeliveryReceiptField.value == "1" &&
objReadReceiptField.value == "1")
{index = 3;}
else if (objReadReceiptField.value == "1")
{index = 1;}
else if (objDeliveryReceiptField.value == "1")
{index = 2;}
composeForm.ReceiptOptions.selectedIndex = index;}

function OnReceiptChange()
{var index = document.MainForm.ReceiptOptions.selectedIndex;if (index == 0)
{objReadReceiptField.value = "0";objDeliveryReceiptField.value = "0";}
else if (index == 1)
{objReadReceiptField.value = "1";objDeliveryReceiptField.value = "0";}
else if (index == 2)
{objReadReceiptField.value = "0";objDeliveryReceiptField.value = "1";}
else if (index == 3)
{objReadReceiptField.value = "1";objDeliveryReceiptField.value = "1";}
}

function OpenGalFind(sType)
{window.open(g_szBase+"/?cmd=galfind&US="+sType,"galfind","toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,width=700,height=500");}
