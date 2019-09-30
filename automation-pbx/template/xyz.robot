*** Settings ***
Documentation     Keywords supported for BOSS portal
...               dev- Kenash, Rahul Doshi, Vasuja
...               Comments:

*** Keywords ***

I Find User With Email ${email}
	&{email}=    Create Dictionary       email=${email}
	add_silent_coach      &{email}
	
