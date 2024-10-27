import threading
import queue
import time
import random
import logging
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)


@dataclass
class TemperatureReading:
    """Represents a temperature reading from a sensor"""
    sensor_id: str
    temperature: float
    timestamp: datetime = datetime.now()

    def __str__(self):
        return (f"Sensor {self.sensor_id}: {self.temperature:.1f}°C "
                f"at {self.timestamp.strftime('%H:%M:%S')}")


class TemperatureSensor(threading.Thread):
    """Producer: Simulates a temperature sensor generating readings"""

    def __init__(self, sensor_id: str, reading_queue: queue.Queue):
        super().__init__(name=f"Sensor-{sensor_id}")
        self.sensor_id = sensor_id
        self.queue = reading_queue
        self.running = True
        self.readings_produced = 0

    def run(self):
        base_temp = random.uniform(20.0, 25.0)  # Base temperature for this sensor

        while self.running:
            # Simulate temperature reading with some variation
            current_temp = base_temp + random.uniform(-0.5, 0.5)
            reading = TemperatureReading(self.sensor_id, current_temp)

            self.queue.put(reading)
            self.readings_produced += 1

            logging.debug(f"Sensor {self.sensor_id} produced: {reading}")
            time.sleep(random.uniform(0.5, 1.5))  # Random interval between readings

    def stop(self):
        self.running = False


class TemperatureProcessor(threading.Thread):
    """Consumer: Processes temperature readings"""

    def __init__(self, worker_id: int, reading_queue: queue.Queue,
                 alert_threshold: float = 26.0):
        super().__init__(name=f"Processor-{worker_id}")
        self.worker_id = worker_id
        self.queue = reading_queue
        self.alert_threshold = alert_threshold
        self.running = True
        self.readings_processed = 0

    def run(self):
        while self.running:
            try:
                # Wait for a reading with timeout
                reading = self.queue.get(timeout=1.0)

                # Process the reading
                self._process_reading(reading)
                self.queue.task_done()
                self.readings_processed += 1

            except queue.Empty:
                continue

    def _process_reading(self, reading: TemperatureReading):
        # Simulate some processing time
        time.sleep(0.1)

        # Check for temperature threshold
        if reading.temperature >= self.alert_threshold:
            logging.warning(
                f"HIGH TEMPERATURE ALERT: {reading}"
            )
        else:
            logging.info(
                f"Processor {self.worker_id} processed: {reading}"
            )

    def stop(self):
        self.running = False


class TemperatureMonitorSystem:
    """Manages the producer-consumer system"""

    def __init__(self, num_sensors: int, num_processors: int,
                 queue_size: Optional[int] = None):
        self.reading_queue = queue.Queue(maxsize=queue_size or 0)
        self.sensors: List[TemperatureSensor] = []
        self.processors: List[TemperatureProcessor] = []

        # Create temperature sensors (producers)
        for i in range(num_sensors):
            sensor = TemperatureSensor(f"S{i + 1}", self.reading_queue)
            self.sensors.append(sensor)

        # Create temperature processors (consumers)
        for i in range(num_processors):
            processor = TemperatureProcessor(i + 1, self.reading_queue)
            self.processors.append(processor)

        self.stats_thread = threading.Thread(
            target=self._print_stats,
            name="StatsReporter"
        )

    def start(self):
        """Start all sensors and processors"""
        logging.info("Starting Temperature Monitoring System")

        # Start processors first
        for processor in self.processors:
            processor.start()

        # Then start sensors
        for sensor in self.sensors:
            sensor.start()

        # Start stats reporting
        self.stats_thread.start()

    def stop(self):
        """Stop all sensors and processors"""
        logging.info("Shutting down Temperature Monitoring System")

        # Stop sensors first
        for sensor in self.sensors:
            sensor.stop()

        # Wait for sensors to finish
        for sensor in self.sensors:
            sensor.join()

        # Wait for queue to be empty
        self.reading_queue.join()

        # Stop processors
        for processor in self.processors:
            processor.stop()

        # Wait for processors to finish
        for processor in self.processors:
            processor.join()

        logging.info("System shutdown complete")

    def _print_stats(self):
        """Periodically print system statistics"""
        while any(sensor.is_alive() for sensor in self.sensors):
            total_produced = sum(s.readings_produced for s in self.sensors)
            total_processed = sum(p.readings_processed for p in self.processors)
            queue_size = self.reading_queue.qsize()

            logging.info(
                f"Stats: Produced={total_produced}, "
                f"Processed={total_processed}, "
                f"Queue Size={queue_size}"
            )

            time.sleep(2)


def main():
    # Create system with 3 sensors and 2 processors
    system = TemperatureMonitorSystem(
        num_sensors=3,
        num_processors=2,
        queue_size=100
    )

    try:
        system.start()

        # Run for 15 seconds
        time.sleep(15)

    finally:
        system.stop()


if __name__ == "__main__":
    main()
