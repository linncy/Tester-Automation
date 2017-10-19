import visa
rm = visa.ResourceManager()
if len(rm.list_resources())==0:
	print('No Device Found.')
else:
	print('Device Found:', rm.list_resources())
try:
	cm22c = rm.open_resource("COM3")
	print("CM22C Successfully Connected")

	lcr4284a = rm.open_resource('GPIB0::17::INSTR')
	print("LCR4284A Successfully Connected")
except:
	print('Error')
	exit()

strInsId_cm22c=cm22c.query("*idn?")
strTempInputA_cm22c=cm22c.query("input? a")
strTemUnitA_cm22c=cm22c.query("input a:units?")
strLoopOnOff_cm22c=cm22c.query("control?")
if(cm22c.query("input a:units k;:*OPC?")):
	print("Input A Unit set to K")
if(cm22c.query("LOOP 1:SETPOINT 273;:*OPC?")):
	print('LOOP 1 Setpoint set to 273')

strInsId_lcr4284a=lcr4284a.query("*idn?")