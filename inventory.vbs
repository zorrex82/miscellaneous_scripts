' Script to generate hardware inventory Windows Version
' Author: Edinor Junior
' Data: 08/07/2019
' Version: 1.0

' Generate file with hostname.
strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2")
Set colItems = objWMIService.ExecQuery( _
"SELECT * FROM Win32_ComputerSystem",,48)
For Each objItem in colItems
NomeComputador = objItem.Caption
Next
'-------- Create file --------------
Dim fso, txtfile
Set fso = CreateObject("Scripting.FileSystemObject")
Set txtfile = fso.CreateTextFile("C:\Users\user\Documents\Scripts_Powershell\" & NomeComputador & ".txt", True) ' Don't forget to change directory
txtfile.Write ("Hardware Report:")
txtfile.WriteBlankLines(3)
'--------------- Software -------------
strComputer = "."
strProperties = "*"'"CSName, Caption, OSType, Version, OSProductSuite, BuildNumber, ProductType, OSLanguage, CSDVersion, InstallDate, RegisteredUser, Organization, SerialNumber, WindowsDirectory, SystemDirectory"
objClass = "Win32_OperatingSystem"
strQuery = "SELECT " & strProperties & " FROM " & objClass
Set colOS = objWMIService.ExecQuery(strQuery, , wbemFlagReturnImmediately + wbemFlagForwardOnly)
For Each objItem in colOS
txtfile.write ("Nome:")
txtfile.WriteBlankLines(1)
txtfile.write (objItem.CSName)
txtfile.WriteBlankLines(1)
txtfile.write ("S.O.:")
txtfile.WriteBlankLines(1)
txtfile.write (objItem.Caption)
txtfile.WriteBlankLines(1)
If SO_Type = 16 Then
SO_Name = "Microsoft Windows 95"
ElseIf SO_Type = 17 Then
SO_Name = "Microsoft Windows 98"
End If
If SO_ProdType = 1 Then
SO_ProdType = "Workstation"
ElseIf SO_ProdType = 2 Then
SO_ProdType = "Domain Control"
ElseIf SO_ProdType = 3 Then
SO_ProdType = "Server"
End If
If SO_Language = 1033 Then
SO_Language = "English - United State"
ElseIf SO_Language = 1046 Then
SO_Language = "Portuguese - Brazil"
Else
SO_Language = "Other Language"
End If
If SO_Suite = 1 Then
SO_Suite = "Small Business"
ElseIf SO_Suite = 2 Then
SO_Suite = "Enterprise"
ElseIf SO_Suite = 4 Then
SO_Suite = "Backoffice"
ElseIf SO_Suite = 8 Then
SO_Suite = "Communication Server"
ElseIf SO_Suite = 16 Then
SO_Suite = "Terminal Server"
ElseIf SO_Suite = 18 Then
SO_Suite = "Enterprise e Terminal Server"
ElseIf SO_Suite = 32 Then
SO_Suite = "Small Business (Restrito)"
ElseIf SO_Suite = 64 Then
SO_Suite = "Embedded NT"
ElseIf SO_Suite = 128 Then
SO_Suite = "Data Center"
ElseIf SO_Suite = 256 Then
SO_Suite = "Single User"
ElseIf SO_Suite = 512 Then
SO_Suite = "Personal"
ElseIf SO_Suite = 1024 Then
SO_Suite = "Blade"
End If
Next
'--------------- User ---------------
txtfile.WriteBlankLines(1)
txtfile.write ("User:")
txtfile.WriteBlankLines(1)
objClass = "Win32_ComputerSystem"
strQuery = "SELECT " & strProperties & " FROM " & objClass
Set colSys = objWMIService.ExecQuery(strQuery, , wbemFlagReturnImmediately + wbemFlagForwardOnly)
For Each objItem in colSys
txtfile.write (objItem.UserName)
txtfile.WriteBlankLines(1)
Next
'------------ Processor ---------------
txtfile.write("Processor:")
txtfile.WriteBlankLines(1)
strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2")
Set colItems = objWMIService.ExecQuery( _
"SELECT * FROM Win32_Processor",,48)
For Each objItem in colItems
'----------- Processor Name --------
txtfile.write (objItem.name)
txtfile.WriteBlankLines(1)
'--------------- Clock ------------------
txtfile.write ("Clock:")
txtfile.WriteBlankLines(1)
txtfile.write (objItem.CurrentClockSpeed & " MHZ")
txtfile.WriteBlankLines(1)
Next
'-------------- Memory -----------------
strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2")
Set colItems = objWMIService.ExecQuery( _
"SELECT * FROM Win32_physicalmemory",,48)
For Each objItem in colItems
'----------  Database name ---------------
txtfile.write ("Memory:")
'------------ Capacity -----------------
txtfile.write ("Capacity:")
txtfile.WriteBlankLines(1)
txtfile.write (objItem.capacity/1048576)
txtfile.WriteBlankLines(1)
Next
'--------------- hd -----------------------
strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2")
Set colItems = objWMIService.ExecQuery( _
"SELECT * FROM Win32_diskdrive",,48)
For Each objItem in colItems
'------------- Drive Name ------------
txtfile.write ("Drive:")
txtfile.WriteBlankLines(1)
txtfile.write (objItem.caption)
txtfile.WriteBlankLines(1)
'------------- Interface ------------------
txtfile.write ("Interface:")
txtfile.WriteBlankLines(1)
txtfile.write (objItem.interfacetype)
txtfile.WriteBlankLines(1)
'------------- Size --------------------
txtfile.write ("Size:")
txtfile.WriteBlankLines(1)
txtfile.write (int(objItem.size/1073741824) & " GB")
txtfile.WriteBlankLines(1)
Next
'----------- Adapter Name --------------
strComputer = "."
strProperties = "Description, MACAddress, IPAddress, IPSubnet, DefaultIPGateway, DNSServerSearchOrder, DNSDomain, DNSDomainSuffixSearchOrder, DHCPEnabled, DHCPServer, WINSPrimaryServer, WINSSecondaryServer, ServiceName"
objClass = "Win32_NetworkAdapterConfiguration"
strQuery = "SELECT " & strProperties & " FROM " & objClass & " WHERE IPEnabled = True AND ServiceName <> 'AsyncMac' AND ServiceName <> 'VMnetx' AND ServiceName <> 'VMnetadapter' AND ServiceName <> 'Rasl2tp' AND ServiceName <> 'PptpMiniport' AND ServiceName <> 'Raspti' AND ServiceName <> 'NDISWan' AND ServiceName <> 'RasPppoe' AND ServiceName <> 'NdisIP' AND ServiceName <> ''"
Set colAdapters = objWMIService.ExecQuery(strQuery, , wbemFlagReturnImmediately + wbemFlagForwardOnly)
'------------ Network --------------------------
For Each objItem in colAdapters
'For Each objItem in colItems
txtfile.write ("Adaptador:")
txtfile.WriteBlankLines(1)
txtfile.write (objItem.Description)
txtfile.WriteBlankLines(1)
'------------ IP --------------------------
txtfile.write ("IP:")
txtfile.WriteBlankLines(1)
IP_Address = objItem.IPAddress
txtfile.write (IP_Address(i))
txtfile.WriteBlankLines(1)
Next