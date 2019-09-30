*** Settings ***


*** Variables ***
# &{port1}          server=localhost           component_type=manhattancomponent             port=4444          browserName=chrome          aut=connect_client        isDevScript=false
&{port1}          server=localhost           component_type=manhattancomponent             port=5555          browserName=chrome          aut=connect_client        isDevScript=false 
&{port2}          server=localhost           component_type=manhattancomponent             port=6666          browserName=chrome          aut=connect_client        isDevScript=false
&{port3}          server=localhost           component_type=manhattancomponent             port=7777          browserName=chrome          aut=connect_client        isDevScript=false
&{port4}          server=localhost           component_type=manhattancomponent             port=8888          browserName=chrome          aut=browser               isDevScript=false
&{port5}          server=localhost           component_type=manhattancomponent             port=9999          browserName=chrome          aut=browser               isDevScript=false
	
${is_runtype_mt}       0

${message}           I*will*call*back 
	
