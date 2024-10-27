# example of a producer-consumer pattern using a temperature sensor simulation system that processes temperature readings.


This example,[solution21.py](solution21.py), implements a temperature monitoring system see details:

1. **Clear Producer-Consumer Separation**:
   - `TemperatureSensor`: Producer that generates temperature readings
   - `TemperatureProcessor`: Consumer that processes readings
   - `TemperatureMonitorSystem`: Manager that coordinates the system

2. **Practical Data Model**:
   - `TemperatureReading` class with sensor ID, temperature, and timestamp
   - Realistic simulation of temperature variations
   - Alert threshold monitoring

3. **System Features**:
   - Multiple producers (sensors) and consumers (processors)
   - Queue-based communication
   - Graceful startup and shutdown
   - Real-time statistics reporting
   - Error handling and logging

4. **Real-world Considerations**:
   - Simulated processing time
   - Random intervals between readings
   - Temperature threshold alerts
   - Queue size monitoring
   - System statistics tracking

To use this system:

```python
# Create system with 3 sensors and 2 processors
system = TemperatureMonitorSystem(
    num_sensors=3,
    num_processors=2,
    queue_size=100
)

# Start the system
system.start()

# Run for some time
time.sleep(15)

# Shutdown
system.stop()
```

The system will:
1. Start multiple temperature sensors that generate readings
2. Process readings using multiple processor threads
3. Log normal readings and alert on high temperatures
4. Provide periodic statistics about the system
5. Shutdown gracefully when requested
