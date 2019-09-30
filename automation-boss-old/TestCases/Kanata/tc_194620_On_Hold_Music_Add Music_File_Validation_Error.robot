*** Settings ***
Documentation  On-Hold Music - Add Music - File Validation Error (tc 194620)

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Env file
Resource          ../../Variables/EnvVariables.robot

#libraries
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           Collections

*** Variables ***
# Validate these wave files to ensure the correct sample range with stereo and mono settings.
${moh_mp3_fail_filePath}=                       ${EXECDIR}${/}Test_files${/}MOH_mp3_fail.mp3
${moh_stereo_below_8khz_wav_filePath}=          ${EXECDIR}${/}Test_files${/}MOH_stereo_below_8khz.wav
${moh_mono_greater_8khz_wav_filePath}=          ${EXECDIR}${/}Test_files${/}MOH_mono_above_8khz.wav
&{file_upload_info_moh_mp3_fail}=               browseButton=OnHoldMusicAddMusicBrowseButton     filePath=${moh_mp3_fail_filePath}
&{file_upload_info_moh_stereo_below_8khz_wav}=  browseButton=OnHoldMusicAddMusicBrowseButton     filePath=${moh_stereo_below_8khz_wav_filePath}
&{file_upload_info_moh_mono_greater_8khz_wav}=  browseButton=OnHoldMusicAddMusicBrowseButton     filePath=${moh_mono_greater_8khz_wav_filePath}

*** Test Cases ***
On-Hold Music - Add Music - File Validation Error (tc 194620)
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    and I open On Hold Music

    When I upload a mp3 file to On Hold Music    &{file_upload_info_moh_mp3_fail}
    Then I verify an error message that the file is in the wrong format
    and I verify this file was not uploaded to On Hold Music  ${moh_mp3_fail_filePath}

    When I upload a stereo below 8khz wav file to On Hold Music    &{file_upload_info_moh_stereo_below_8khz_wav}
    Then I verify this file was successfully uploaded to On Hold Music  &{file_upload_info_moh_stereo_below_8khz_wav}

    When I upload a mono above 8khz wav file to On Hold Music    &{file_upload_info_moh_mono_greater_8khz_wav}
    Then I verify this file was successfully uploaded to On Hold Music  &{file_upload_info_moh_mono_greater_8khz_wav}

    # Verification on ShoreTel Director on the Cosmo server cannot be performed since Kanata team doesn't have access.

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

