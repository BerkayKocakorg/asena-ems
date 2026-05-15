package com.asena.asenaems.controller;

import com.asena.asenaems.dto.PredictionDTO;
import com.asena.asenaems.dto.TelemetryDTO;
import com.asena.asenaems.service.TelemetryService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin("*")
public class TelemetryController {

    private final TelemetryService telemetryService;

    public TelemetryController(TelemetryService telemetryService) {
        this.telemetryService = telemetryService;
    }

    @PostMapping("/telemetry")
    public void receiveTelemetry(@RequestBody TelemetryDTO data) {
        telemetryService.processTelemetry(data);
    }

    @GetMapping("/victims")
    public List<PredictionDTO> getVictims() {
        return telemetryService.getVictims();
    }
}