# Edited from Source - https://stackoverflow.com/a/38457505

Function WindowsUpdate {
Write-Output "Starting Windows Update check"
$Criteria = "IsInstalled=0 and Type='Software'"
$Searcher = New-Object -ComObject Microsoft.Update.Searcher
Write-Output "$Searcher"
$StartTime = Get-Date
Write-Output "$StartTime"
try {
    $SearchResult = $Searcher.Search($Criteria).Updates
    if($SearchResult.Count -eq 0) {
        Write-Output "There are no applicable updates found."
    }
    else {
        $Session = New-Object -ComObject Microsoft.Update.Session
	Write-Output "Session: $Session"
        $Downloader = $Session.CreateUpdateDownloader()
        $Downloader.Updates = $SearchResult
        $DownloadResult = $Downloader.Download()
	if($DownloadResult.ResultCode -ne 2) {
		Write-Output "Problem with download (code $($DownloadResult.ResultCode))"
		return
	}
        $Installer = New-Object -ComObject Microsoft.Update.Installer
        $Installer.Updates = $SearchResult
        $Result = $Installer.Install()

        if($Result.ResultCode -eq 2) { 
            Write-Output "Following Updates Successful"
            $SearchResult | ForEach-Object { $_.Title }
            if($Result.RebootRequired) {
                #Write-Output "Restart required to finish installing and will occur in 3 minutes.  Please save work."
                #shutdown /r /t 180
            }
        }
        else {
            Start-Sleep -Seconds 5
            $ThisHistory = CompleteUpdateHistory | Where-Object { $_.Date -ge $StartTime.ToUniversalTime() }
            Write-Output "There was a problem with updating.  Here is a rundown of what occurred.  Please copy and paste for IT."
            $ThisHistory
            if($Result.RebootRequired) { Write-Output "Just a head's up, your computer requires a restart before finishing successful updates." }
        }
    }    
}
catch {
    Write-Output "There was an error. $($_.Exception.Message)"
    }
}

Function CompleteUpdateHistory {
    $Session = New-Object -ComObject "Microsoft.Update.Session"
    $Searcher = $Session.CreateUpdateSearcher()
    $HistoryCount = $Searcher.GetTotalHistoryCount()

    $Searcher.QueryHistory(0, $HistoryCount) | Select-Object Title, Date,
        @{name="Status"; expression={
            switch($_.ResultCode){
                0 {"NotStarted"}
                1 {"InProgress"}
                2 {"Completed Successfully"}
                3 {"Completed with errors"}
                4 {"Failed"}
                5 {"Aborted"}
                default {"Unknown"}
            }
        }}
}

Function UpdateTest {
    $Searcher = New-Object -ComObject Microsoft.Update.Searcher
    $Results = $Searcher.Search("IsInstalled=0 and Type='Software'").Updates
    $Results.Count
    $Results | ForEach-Object { $_.Title }
}

#This opens up complete update history into a GUI that is easy to read
#CompleteUpdateHistory | Out-GridView

#This allows ps1 scripts to run for one session
#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass