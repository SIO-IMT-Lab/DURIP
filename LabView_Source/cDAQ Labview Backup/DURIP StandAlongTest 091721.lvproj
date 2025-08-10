<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="23008000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">false</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Project Documentation" Type="Folder">
			<Item Name="Documentation Images" Type="Folder">
				<Item Name="real-time_waveform_acq_logging.png" Type="Document" URL="../../LabVIEW Data/DURIP TestBench Hello World/images/real-time_waveform_acq_logging.png"/>
				<Item Name="loc_rt_waveform_acq_daqmx.gif" Type="Document" URL="../../LabVIEW Data/DURIP TestBench Hello World/documentation/loc_rt_waveform_acq_daqmx.gif"/>
			</Item>
			<Item Name="LabVIEW Real-Time Waveform Acquisition and Logging (NI-DAQmx) Documentation.html" Type="Document" URL="../../LabVIEW Data/DURIP TestBench Hello World/documentation/LabVIEW Real-Time Waveform Acquisition and Logging (NI-DAQmx) Documentation.html"/>
		</Item>
		<Item Name="Error Handlers" Type="Folder">
			<Item Name="UI Error Handler - Message Handler.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/UI Error Handlers/UI Error Handler - Message Handler.vi"/>
			<Item Name="UI Error Handler - Monitoring.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/UI Error Handlers/UI Error Handler - Monitoring.vi"/>
		</Item>
		<Item Name="Globals" Type="Folder">
			<Item Name="Global - All UI Loop Stop.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/Globals/Global - All UI Loop Stop.vi"/>
			<Item Name="Global - Configuration Options.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/Globals/Global - Configuration Options.vi"/>
			<Item Name="Global - UI Stream and Variable Connections.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/Globals/Global - UI Stream and Variable Connections.vi"/>
		</Item>
		<Item Name="Support VIs" Type="Folder">
			<Property Name="NI.SortType" Type="Int">3</Property>
			<Item Name="Message Queue.lvlib" Type="Library" URL="../../LabVIEW Data/DURIP TestBench Hello World/support/Message Queue/Message Queue.lvlib"/>
			<Item Name="User Event - Stop.lvlib" Type="Library" URL="../../LabVIEW Data/DURIP TestBench Hello World/support/User Event - Stop/User Event - Stop.lvlib"/>
			<Item Name="Check Loop Error.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/support/Check Loop Error.vi"/>
			<Item Name="Close Variable Connections.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/support/Close Variable Connections.vi"/>
			<Item Name="Set Enable State on Multiple Controls.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/support/Set Enable State on Multiple Controls.vi"/>
			<Item Name="UI - Initiate Connection.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/support/UI - Initiate Connection.vi"/>
			<Item Name="UI - Read Stream from RT.vi" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/support/UI - Read Stream from RT.vi"/>
		</Item>
		<Item Name="Type Definitions" Type="Folder">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Item Name="Acquisition and Logging Configuration.ctl" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/controls/Acquisition and Logging Configuration.ctl"/>
			<Item Name="Error Type.ctl" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/controls/Error Type.ctl"/>
			<Item Name="TDMS Properties.ctl" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/controls/TDMS Properties.ctl"/>
			<Item Name="UI Data.ctl" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/controls/UI Data.ctl"/>
			<Item Name="Variable References.ctl" Type="VI" URL="../../LabVIEW Data/DURIP TestBench Hello World/controls/Variable References.ctl"/>
		</Item>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Generic Real-Time Waveform Acquisition and Logging UI" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{C554F6E6-4FFF-4E5D-ABE6-305E9DDA0A26}</Property>
				<Property Name="App_INI_GUID" Type="Str">{62464553-0192-49ED-AE9B-16658031A9C9}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="App_serverType" Type="Int">1</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{4F04A458-D5C2-4E35-B26E-367FDC9017D9}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Generic Real-Time Waveform Acquisition and Logging UI</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/NI_AB_PROJECTNAME/Generic Real-Time Waveform Acquisition and Logging UI</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{DAAD6869-BBB9-4FC1-8BFC-D6C3006A19BA}</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">GenericRealTimeWaveformAcquisitionandLogging UI.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/Generic Real-Time Waveform Acquisition and Logging UI/GenericRealTimeWaveformAcquisitionandLogging UI.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/Generic Real-Time Waveform Acquisition and Logging UI/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{DAFA3238-037F-4E96-BFFC-C2E22AAACD6E}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref"></Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Generic Real-Time Waveform Acquisition and Logging UI</Property>
				<Property Name="TgtF_internalName" Type="Str">Generic Real-Time Waveform Acquisition and Logging UI</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2012 </Property>
				<Property Name="TgtF_productName" Type="Str">Generic Real-Time Waveform Acquisition and Logging UI</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{6CFF9783-C161-496B-969E-D5C2E2E632BC}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">GenericRealTimeWaveformAcquisitionandLogging UI.exe</Property>
			</Item>
		</Item>
	</Item>
	<Item Name="NI-cDAQ-9136-01BD035E" Type="RT CDAQ Chassis">
		<Property Name="alias.name" Type="Str">NI-cDAQ-9136-01BD035E</Property>
		<Property Name="alias.value" Type="Str">172.22.11.2</Property>
		<Property Name="CCSymbols" Type="Str">OS,Linux;CPU,x64;TARGET_TYPE,RT;</Property>
		<Property Name="host.ResponsivenessCheckEnabled" Type="Bool">true</Property>
		<Property Name="host.ResponsivenessCheckPingDelay" Type="UInt">5000</Property>
		<Property Name="host.ResponsivenessCheckPingTimeout" Type="UInt">1000</Property>
		<Property Name="host.TargetCPUID" Type="UInt">9</Property>
		<Property Name="host.TargetOSID" Type="UInt">19</Property>
		<Property Name="nidaqmx.ControllerPID" Type="Str">7833</Property>
		<Property Name="target.cleanupVisa" Type="Bool">false</Property>
		<Property Name="target.FPProtocolGlobals_ControlTimeLimit" Type="Int">300</Property>
		<Property Name="target.getDefault-&gt;WebServer.Port" Type="Int">80</Property>
		<Property Name="target.getDefault-&gt;WebServer.Timeout" Type="Int">60</Property>
		<Property Name="target.IOScan.Faults" Type="Str"></Property>
		<Property Name="target.IOScan.NetVarPeriod" Type="UInt">100</Property>
		<Property Name="target.IOScan.NetWatchdogEnabled" Type="Bool">false</Property>
		<Property Name="target.IOScan.Period" Type="UInt">10000</Property>
		<Property Name="target.IOScan.PowerupMode" Type="UInt">0</Property>
		<Property Name="target.IOScan.Priority" Type="UInt">0</Property>
		<Property Name="target.IOScan.ReportModeConflict" Type="Bool">true</Property>
		<Property Name="target.IsRemotePanelSupported" Type="Bool">true</Property>
		<Property Name="target.RTCPULoadMonitoringEnabled" Type="Bool">true</Property>
		<Property Name="target.RTDebugWebServerHTTPPort" Type="UInt">8001</Property>
		<Property Name="target.RTTarget.ApplicationPath" Type="Path">/home/lvuser/natinst/bin/startup.rtexe</Property>
		<Property Name="target.RTTarget.EnableFileSharing" Type="Bool">true</Property>
		<Property Name="target.RTTarget.IPAccess" Type="Str">+*</Property>
		<Property Name="target.RTTarget.LaunchAppAtBoot" Type="Bool">true</Property>
		<Property Name="target.RTTarget.VIPath" Type="Path">/home/lvuser/natinst/bin</Property>
		<Property Name="target.server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="target.server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="target.server.tcp.access" Type="Str">+*</Property>
		<Property Name="target.server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="target.server.tcp.paranoid" Type="Bool">true</Property>
		<Property Name="target.server.tcp.port" Type="Int">3363</Property>
		<Property Name="target.server.tcp.serviceName" Type="Str"></Property>
		<Property Name="target.server.tcp.serviceName.default" Type="Str">Main Application Instance/VI Server</Property>
		<Property Name="target.server.vi.access" Type="Str">+*</Property>
		<Property Name="target.server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="target.server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="target.server.viscripting.showScriptingOperationsInContextHelp" Type="Bool">false</Property>
		<Property Name="target.server.viscripting.showScriptingOperationsInEditor" Type="Bool">false</Property>
		<Property Name="target.WebServer.Config" Type="Str"># Web server configuration file.
# Generated by LabVIEW 19.0f2
# 2/13/2020 10:29:21 AM

#
# Global Directives
#
NI.AddLVRouteVars
TypesConfig "$LVSERVER_CONFIGROOT/mime.types"
LimitWorkers 10
LoadModulePath "$LVSERVER_MODULEPATHS"
LoadModule LVAuth lvauthmodule
LoadModule LVRFP lvrfpmodule
Listen 8000

#
# Directives that apply to the default server
#
NI.ServerName LabVIEW
DocumentRoot "$LVSERVER_DOCROOT"
InactivityTimeout 60
SetConnector netConnector
AddHandler LVAuth
AddHandler LVRFP
AddHandler fileHandler ""
AddOutputFilter chunkFilter
DirectoryIndex index.htm
</Property>
		<Property Name="target.WebServer.Enabled" Type="Bool">false</Property>
		<Property Name="target.WebServer.LogEnabled" Type="Bool">false</Property>
		<Property Name="target.WebServer.LogPath" Type="Path">/c/ni-rt/system/www/www.log</Property>
		<Property Name="target.WebServer.Port" Type="Int">80</Property>
		<Property Name="target.WebServer.RootPath" Type="Path">/c/ni-rt/system/www</Property>
		<Property Name="target.WebServer.TcpAccess" Type="Str">c+*</Property>
		<Property Name="target.WebServer.Timeout" Type="Int">60</Property>
		<Property Name="target.WebServer.ViAccess" Type="Str">+*</Property>
		<Property Name="target.webservices.SecurityAPIKey" Type="Str">PqVr/ifkAQh+lVrdPIykXlFvg12GhhQFR8H9cUhphgg=:pTe9HRlQuMfJxAG6QCGq7UvoUpJzAzWGKy5SbZ+roSU=</Property>
		<Property Name="target.webservices.ValidTimestampWindow" Type="Int">15</Property>
		<Item Name="cDAQ Blinky.vi" Type="VI" URL="../cDAQ Blinky.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="ni_emb.dll" Type="Document" URL="/&lt;vilib&gt;/ni_emb.dll"/>
				<Item Name="NI_Real-Time Target Support.lvlib" Type="Library" URL="/&lt;vilib&gt;/NI_Real-Time Target Support.lvlib"/>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="cDAQBlinky" Type="{69A947D5-514E-4E75-818E-69657C0547D8}">
				<Property Name="App_INI_aliasGUID" Type="Str">{978B4DC7-6CB8-4175-B9F3-45641EF0F2D3}</Property>
				<Property Name="App_INI_GUID" Type="Str">{371F6880-8A97-4B6D-919B-BF978E458AE9}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="App_serverType" Type="Int">0</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{6CBB2091-C9AC-4D5E-9D25-8C0AD2BBB14B}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">cDAQBlinky</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/NI_AB_PROJECTNAME/NI_AB_TARGETNAME/cDAQBlinky</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{3CA4A0D8-DE8A-4D4B-B36D-1EAC7127015F}</Property>
				<Property Name="Bld_targetDestDir" Type="Path">/home/lvuser/natinst/bin</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">startup.rtexe</Property>
				<Property Name="Destination[0].path" Type="Path">/home/lvuser/natinst/bin/startup.rtexe</Property>
				<Property Name="Destination[0].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">/home/lvuser/natinst/bin/data</Property>
				<Property Name="Destination[1].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{7F1020A3-FF2B-45C8-8245-BA1234E36367}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/NI-cDAQ-9136-01BD035E/cDAQ Blinky.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">Scripps Institution of Oceanography</Property>
				<Property Name="TgtF_fileDescription" Type="Str">cDAQBlinky</Property>
				<Property Name="TgtF_internalName" Type="Str">cDAQBlinky</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2023 Scripps Institution of Oceanography</Property>
				<Property Name="TgtF_productName" Type="Str">cDAQBlinky</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{8C7BB7EF-3AAB-459D-8F68-F9EE2FDA9720}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">startup.rtexe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
		</Item>
	</Item>
</Project>
