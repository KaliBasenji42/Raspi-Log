import time

# Variables

run = True

cont = 0

# Defaults

values = {

  'path': '/sys/class/thermal/thermal_zone0/temp',
  'scale': 1000,
  'method': 0,
  'methodInfo': [],

  'spf': 1.0,
  'logLen': 20.0,

  'barMin': 20.0,
  'barMax': 100.0,
  'barLen': 50.0,
  'barMed': .7,
  'barHi': .85,
  'barChr': '=',
  'barLoC': 32.0,
  'barMedC': 33.0,
  'barHiC': 31.0
  
}

# Keys

types = {
  'thermal': ['/sys/class/thermal/thermal_zone0/temp',
              1000,
              0,
              [],
              'CPU temp in Celcius'],
  'cpughz': ['/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq',
             1000000,
             0,
             [],
             'CPU Clocking in GHz. "cpu0" can be interchanged for different CPU'],
  'netrx': ['/sys/class/net/eth0/statistics/rx_bytes',
             1048576,
             0,
             [],
             'MB received. "eth0" can be interchanged for different network device'],
  'nettx': ['/sys/class/net/eth0/statistics/tx_bytes',
             1048576,
             0,
             [],
             'MB transmitted. "eth0" can be interchanged for different network device']
}

colorKey = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']

# Function

def strToFloat(string):
  
  numStr = ''
  
  for i in range(len(string)):
    
    if string[i].isnumeric(): numStr = numStr + string[i]
    if string[i] == '.': numStr = numStr + string[i]
    
  
  if len(numStr) == 0: return 0
  
  if string[0] == '-': return -1 * float(numStr)
  else: return float(numStr)
  

def strToArray(string):
  
  out = []
  
  var = ''
  
  div = ' '
  
  string = string + div
  
  for i in range(len(string)):
    
    if string[i-len(div):i] == div:
      
      var = var[:-len(div)]
      
      out.append(var)
      
      var = ''
      
    
    var += string[i]
    
  
  var = var[:-len(div)]
  
  out.append(var)
  
  return out
  

def lenNum(string, length): # Adds 0's to string until at length
  
  add = length - len(string)
  
  out = string
  
  for i in range(add): out = out + '0'
  
  return out
  

def bar(val, minimum, maximum, length, medium, high, char, loColor, medColor, hiColor):
  
  # Validating
  
  val = max(min(val, maximum), minimum)
  
  length = int(max(length, 0))
  
  loColor = int(max(min(loColor, 36), 31))
  medColor = int(max(min(medColor, 36), 31))
  hiColor = int(max(min(hiColor, 36), 31))
  
  # Variables
  
  val = val - minimum
  
  span = maximum - minimum
  
  barLen = round((val / span) * length)
  
  # Output
  
  out = str(minimum) +  '[\033[' + str(loColor) + 'm'
  
  for i in range(barLen):
    
    if i / length >= high: out = out + '\033[' + str(hiColor) + 'm'
    elif i / length >= medium: out = out + '\033[' + str(medColor) + 'm'
    
    out = out + char
    
  
  for i in range(length - barLen): out = out + ' '
  
  out = out + '\033[0m]' + str(maximum)
  
  return out
  

def printLog(log, new):
  
  # Roll
  
  log.pop(0)
  
  log.append(new)
  
  # Print
  
  for entry in log: print('\033[F', end = '')
  
  for entry in log: print('\r' + entry, end = '\n')
  
  return log
  

def getCont(path, method, methodInfo):
  
  out = 0
  
  if method == 0:
    
    with open(path, 'r') as file: out = strToFloat(file.read())
    
  
  return out / values['scale']

# Instructions

print('Inputs:')
print('  Case does not matter')
print('  Numbers are validated before use')
print('    (if logLen is set to -5.2 it will be treated as 1)')
print()
print('  "quit": Quits')
print('  "run": Run graph loop (must kill program to stop)')
print('  "spf": Seconds per frame for graph, Default: 1')
print('  "logLen": How many lines are recorded, Default: 20')
print()
print('  "path": File path for data file, Defualt: (for thermal)')
print('  "scale": Scale of return value, Default: 1000')
print('  "method": Method for gathering info, Default: 0')
print('    0: Raw')
print('    1: Inverse, (total - raw) / total')
print('    2: Divide by time, (new - old) / "spf"')
print('  "methodInfo": Other info needed for gathering data, Default: []')
print('    0: []')
print('    1: [totalName, rawName]')
print('    2: [old]')
print('  "type": Looks up paths saved in list for data file')
print('  "type?": Print types in array noted above')
print()
print('  "barMin": Default: 20')
print('  "barMax": Default: 100')
print('  "barLen": number of chars in bar, Default: 50')
print('  "barMed": Medium Threshold (0 to 1), Default: 0.7')
print('  "barHi": High Threshold (0 to 1), Default: 0.85')
print('  "barChr": Character used in bar, Default: "="')
print('  "barLoC": Low color, Default: 32 (green)')
print('  "barMedC": Medium color, Default: 33 (yellow)')
print('  "barHiC": High color, Default: 31 (red)')
print('  "c?": Print color key')

# Try File

try:
  with open(values['path'], 'r') as file: pass
except:
  print('\nUnable to Open :/')
  run = False

# Input Loop

while True:
  
  print()
  inp = input('Input: ')
  print()
  
  inp = inp.lower()
  
  # Quit and Run
  
  if inp == 'quit':
    run = False
    break
  
  elif inp == 'run':
    
    if run: break
    
    print('Error')
    
  
  # Info
  
  elif inp == 'type?':
    for key in types: print(key + ': ' + types[key][0] +
                            ', scale: ' + str(types[key][1]) +
                            '\n  ' + types[key][2])
  
  elif inp == 'c?':
    for i in range(len(colorKey)): print(colorKey[i] + ': ' + str(i+31))
  
  # Type
  
  elif inp == 'type':
    
    valInp = input('"type": ')
    print()
    
    for key in types:
      
      if valInp == key:
        
        try:
          with open(types[key][0], 'r') as file: pass
        except:
          print('Unable to Open :/')
          run = False
        else:
          values['path'] = types[key][0]
          print('"path" set to "' + values['path'] + '"')
          
          values['scale'] = types[key][1]
          print('"scale" set to "' + str(values['scale']) + '"')
        
      
    
  
  # String Input
  
  elif inp == 'path':
    
    valInp = input('"path": ')
    print()
    
    try:
      with open(inp, 'r') as file: pass
    except:
      print('Unable to Open :/')
      run = False
    else:
      values['path'] = valInp
      print('"path" set to "' + values['path'] + '"')
    
  
  elif inp == 'barchr':
    
    valInp = input('"barChr": ')
    print()
    
    values['barChr'] = (valInp + ' ')[0]
    print('"barChr" set to "' + values['barChr'] + '"')
    
  
  # Method Info / Array Input
  
  elif inp == "methodinfo":
    
    valInp = input('"methodInp: ')
    print()
    
    values['methodInfo'] = strToArray(valInp)
    print('"methodInfo" set to "' + values['methodInfo'] + '"')
    
  
  # All Other
  
  else:
    
    for key in values:
      
      if inp == key.lower():
        
        valInp = input('"' + key + '": ')
        print()
        
        values[key] = strToFloat(valInp)
        
        print('"' + key +'" set to "' + str(values[key]) + '"')
        
    
  

# Preloop

contLog = [''] * int(max(values['logLen'], 1))

print('Press [CTRL] + [C] to stop')

for entry in contLog: print('')

# Graph Loop

while run:
  
  # Read
  
  cont = getCont(values['path'], values['method'], values['methodInfo'])
  
  # Print
  
  newLog = bar(cont, 
               values['barMin'],
               values['barMax'],
               values['barLen'],
               values['barMed'],
               values['barHi'],
               values['barChr'],
               values['barLoC'],
               values['barMedC'],
               values['barHiC'])
  
  newLog = newLog + ' | ' + lenNum(str(cont), 5) + '  '
  
  contLog = printLog(contLog, newLog)
  
  # Time
  
  time.sleep(max(values['spf'], 0))
  
