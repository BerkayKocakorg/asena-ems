package com.asena.asenaems.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class PredictionDTO {
    // Sinan Python'da 'target_lat' gönderse bile Java bunu 'targetLat' içine koyacak
    @JsonProperty("targetLat")
    private double targetLat;

    @JsonProperty("targetLon")
    private double targetLon;

    @JsonProperty("status")
    private int status;
}