#LIBRERIAS.
import psutil #pip install psutil
import platform


entrada = open("SystemInformation.txt",'w')

#FUNCION PARA REPRESENTAR TAMAÑOS EN BITS.
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

#INFORMACIÓN BÁSICA DEL SISTEMA.
entrada.write("***** System Information *****\n")
uname = platform.uname()
entrada.write(f"System: {uname.system} \n")
entrada.write(f"Node Name: {uname.node}\n")
entrada.write(f"Release: {uname.release}\n")
entrada.write(f"Version: {uname.version}\n")
entrada.write(f"Machine: {uname.machine}\n")
entrada.write(f"Processor: {uname.processor}\n")
entrada.write("\n")

#INFORMACIÓN DE LA CPU
entrada.write("***** CPU Info *****\n")
#Nº NUCLEOS
entrada.write("Physical cores:"+ str(psutil.cpu_count(logical=False)) +"\n")
entrada.write("Total cores:"+ str(psutil.cpu_count(logical=True)) +"\n")


#FRECUENCIAS CPU
cpufreq = psutil.cpu_freq()
entrada.write(f"Max Frequency: {cpufreq.max:.2f}Mhz"+"\n")
entrada.write(f"Min Frequency: {cpufreq.min:.2f}Mhz"+"\n")
entrada.write(f"Current Frequency: {cpufreq.current:.2f}Mhz"+"\n")
entrada.write("\n")

#USO DE CPU
entrada.write("CPU Usage Per Core:"+"\n")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
    entrada.write(f"Core {i}: {percentage}%"+"\n")
entrada.write(f"Total CPU Usage: {psutil.cpu_percent()}%"+"\n")
entrada.write("\n")


#MEMORIA
entrada.write("***** Memory Information *****\n")
svmem = psutil.virtual_memory()
entrada.write(f"Total: {get_size(svmem.total)}"+"\n")
entrada.write(f"Available: {get_size(svmem.available)}"+"\n")
entrada.write(f"Used: {get_size(svmem.used)}"+"\n")
entrada.write(f"Percentage: {svmem.percent}%"+"\n")
entrada.write( " ***** SWAP *****\n")
swap = psutil.swap_memory()
entrada.write(f"Total: {get_size(swap.total)}"+"\n")
entrada.write(f"Free: {get_size(swap.free)}"+"\n")
entrada.write(f"Used: {get_size(swap.used)}"+"\n")
entrada.write(f"Percentage: {swap.percent}%"+"\n")
entrada.write("\n")

#INFORMACIÓN DEL DISCO DURO
entrada.write("***** Disk Information *****\n")
entrada.write("***** Partitions and Usage: *****\n")
partitions = psutil.disk_partitions()
for partition in partitions:
    entrada.write(f"=== Device: {partition.device} ==="+"\n")
    entrada.write(f"  Mountpoint: {partition.mountpoint}"+"\n")
    entrada.write(f"  File system type: {partition.fstype}"+"\n")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue
    entrada.write(f"  Total Size: {get_size(partition_usage.total)}"+"\n")
    entrada.write(f"  Used: {get_size(partition_usage.used)}"+"\n")
    entrada.write(f"  Free: {get_size(partition_usage.free)}"+"\n")
    entrada.write(f"  Percentage: {partition_usage.percent}%"+"\n")
disk_io = psutil.disk_io_counters()
entrada.write(f"Total read: {get_size(disk_io.read_bytes)}"+"\n")
entrada.write(f"Total write: {get_size(disk_io.write_bytes)}"+"\n")
entrada.write("\n")

#INFORMACIÓN DE REDES
entrada.write("***** Network Information *****\n")
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        entrada.write(f"=== Interface: {interface_name} ==="+"\n")
        if str(address.family) == 'AddressFamily.AF_INET':
            entrada.write(f"  IP Address: {address.address}"+"\n")
            entrada.write(f"  Netmask: {address.netmask}"+"\n")
            entrada.write(f"  Broadcast IP: {address.broadcast}"+"\n")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            entrada.write(f"  MAC Address: {address.address}"+"\n")
            entrada.write(f"  Netmask: {address.netmask}"+"\n")
            entrada.write(f"  Broadcast MAC: {address.broadcast}"+"\n")
net_io = psutil.net_io_counters()
entrada.write(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}"+"\n")
entrada.write(f"Total Bytes Received: {get_size(net_io.bytes_recv)}"+"\n")

