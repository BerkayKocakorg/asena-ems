package com.asena.asenaems.service;

import com.asena.asenaems.dto.PredictionDTO;
import com.asena.asenaems.dto.TelemetryDTO;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;

@Service
public class TelemetryService {
    private final List<PredictionDTO> victims = new ArrayList<>();
    private final SimpMessagingTemplate messagingTemplate;
    private final RestTemplate restTemplate;

    public TelemetryService(SimpMessagingTemplate messagingTemplate) {
        this.messagingTemplate = messagingTemplate;

        // ZAMAN AŞIMI AYARI: Sinan'ı en fazla 1 saniye bekle, sistem kilitlenmesin
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(1000);
        factory.setReadTimeout(1000);
        this.restTemplate = new RestTemplate(factory);
    }

    public void processTelemetry(TelemetryDTO telemetryData) {
        // Sinan'ın (AI) IP adresi ve Flask endpoint'i
        String aiUrl = "http://10.124.242.12:5000/predict";

        try {
            // SİNAN'A VERİYİ GÖNDER VE CEVABI AL
            PredictionDTO prediction = restTemplate.postForObject(aiUrl, telemetryData, PredictionDTO.class);

            if (prediction != null) {
                victims.add(prediction);
                // WebSocket ile canlı yayın
                messagingTemplate.convertAndSend("/topic/victims", prediction);
            }
        } catch (Exception e) {
            // Hata olursa konsola bas ama sistemi durdurma
            System.err.println("AI Haberleşme Hatası: " + e.getMessage());
        }
    }

    public List<PredictionDTO> getVictims() {
        return victims;
    }
}