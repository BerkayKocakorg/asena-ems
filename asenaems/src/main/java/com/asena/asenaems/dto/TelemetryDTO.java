package com.asena.asenaems.dto;

import lombok.Data;

@Data
public class TelemetryDTO {
    private double sensorLat;
    private double sensorLon;
    private String mac;
    private double rssi;
    private long timestamp;
}