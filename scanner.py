import socket
import threading
from queue import Queue
from tqdm import tqdm

def scan_port(host, port, open_ports, progress_bar):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        try:
            if sock.connect_ex((host, port)) == 0:
                open_ports.append(port)
        except socket.error:
            pass
        finally:
            progress_bar.update(1)

def port_scanner(host, start_port=1, end_port=1024, num_threads=100):
    open_ports = []
    port_queue = Queue()

    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    with tqdm(total=port_queue.qsize(), desc="Сканирование портов", unit="порт") as progress_bar:
        def worker():
            while not port_queue.empty():
                port = port_queue.get()
                scan_port(host, port, open_ports, progress_bar)
                port_queue.task_done()

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        port_queue.join()

    print("\nОткрытые порты:")
    for port in sorted(open_ports):
        print(f"Порт {port} открыт")

if __name__ == "__main__":
    target_host = input("Введите имя хоста или IP адрес для сканирования:")
    try:
        port_scanner(target_host)
    except KeyboardInterrupt:
        print("\nСканирование прервано пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
