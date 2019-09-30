*** Variables ***
#################################################
#O Hold Music
#Keys: musicDescription
&{on_hold_music_staff_delete}	 musicDescription=Staff_music_{rand_str}    rename_musicDescription=Staff_music_rename_{rand_str}    filePath=${EXECDIR}${/}Test_files${/}AA-audio_1.wav    verify=
&{on_hold_music_staff_add}	 musicDescription=Staff_music_{rand_str}    rename_musicDescription=Staff_music_rename_{rand_str}    filePath=${EXECDIR}${/}Test_files${/}AA-audio_2.wav    verify=
&{on_hold_music_staff_rename}	 musicDescription=Staff_music_{rand_str}    rename_musicDescription=Staff_music_rename_{rand_str}    filePath=${EXECDIR}${/}Test_files${/}AA-audio_3.wav    verify=
&{on_hold_music_DM_delete}	 musicDescription=DM_music_{rand_str}    rename_musicDescription=DM_music_rename_{rand_str}    filePath=${EXECDIR}${/}Test_files${/}AA-audio_4.wav
&{on_hold_music_DM_add}	 musicDescription=DM_music_{rand_str}    rename_musicDescription=DM_music_rename_{rand_str}    filePath=${EXECDIR}${/}Test_files${/}AA-audio_5.wav
&{on_hold_music_DM_rename}	 musicDescription=DM_music_{rand_str}    rename_musicDescription=DM_music_rename_{rand_str}    filePath=${EXECDIR}${/}Test_files${/}AA-audio_6.wav