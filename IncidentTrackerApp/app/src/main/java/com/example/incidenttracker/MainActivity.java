package com.example.incidenttracker;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * P6 - IncidentTracker MainActivity
 *
 * CONNEXIÓ: Usa 10.0.2.2:8000 per arribar al Django del PC host
 *           (10.0.2.2 = localhost del PC vist des de l'emulador Android)
 *
 * PART 2: Implementa petició HTTP via HttpURLConnection (sense dependències externes)
 */
public class MainActivity extends AppCompatActivity {

    // PART 2: IP especial de l'emulador per accedir al PC host
    // localhost = el propi mòbil → NO funciona
    // 10.0.2.2  = el PC on corre Django → ✅ CORRECTE
    private static final String API_URL = "http://10.0.2.2:8000/api/incidents/";

    private Button btnObtenir;
    private ProgressBar progressBar;
    private TextView tvStatus;
    private TextView tvIncidentsList;

    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final Handler mainHandler = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btnObtenir = findViewById(R.id.copernic_button);
        progressBar = findViewById(R.id.progress_bar);
        tvStatus = findViewById(R.id.tv_status);
        tvIncidentsList = findViewById(R.id.tv_incidents_list);

        btnObtenir.setOnClickListener(v -> fetchIncidents());
    }

    /**
     * Fa la petició HTTP a l'API de Django i mostra els incidents.
     * Usa un thread separat per no bloquejar la UI.
     */
    private void fetchIncidents() {
        btnObtenir.setEnabled(false);
        progressBar.setVisibility(View.VISIBLE);
        tvStatus.setText("Connectant a Django API...");
        tvIncidentsList.setText("");

        executor.execute(() -> {
            String result;
            try {
                // HTTP GET a http://10.0.2.2:8000/api/incidents/
                URL url = new URL(API_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(10000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Accept", "application/json");

                int responseCode = conn.getResponseCode();
                if (responseCode == 200) {
                    BufferedReader reader = new BufferedReader(
                            new InputStreamReader(conn.getInputStream())
                    );
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line);
                    }
                    reader.close();
                    result = parseIncidents(sb.toString());
                } else {
                    result = "Error HTTP: " + responseCode;
                }
                conn.disconnect();

            } catch (Exception e) {
                result = "❌ Error de connexió:\n" + e.getMessage() +
                         "\n\nComprova:\n• Django actiu a localhost:8000\n• L'emulador usa 10.0.2.2";
            }

            final String finalResult = result;
            mainHandler.post(() -> {
                progressBar.setVisibility(View.GONE);
                btnObtenir.setEnabled(true);
                tvStatus.setText("✅ Dades rebudes de PostgreSQL via Django");
                tvIncidentsList.setText(finalResult);
            });
        });
    }

    /**
     * Parseja el JSON de l'API i retorna text formatat per mostrar.
     */
    private String parseIncidents(String jsonStr) {
        try {
            JSONObject root = new JSONObject(jsonStr);
            JSONArray incidents = root.getJSONArray("incidents");
            int total = root.getInt("total");

            if (total == 0) {
                return "⚠️ Cap incident trobat a la base de dades.\nCrea'n un des de l'Admin de Django.";
            }

            StringBuilder sb = new StringBuilder();
            sb.append("📋 Total: ").append(total).append(" incidents\n");
            sb.append("─────────────────────────────\n\n");

            for (int i = 0; i < incidents.length(); i++) {
                JSONObject inc = incidents.getJSONObject(i);
                sb.append("🔴 ").append(inc.getString("title")).append("\n");
                sb.append("   Severitat: ").append(inc.getString("severity")).append("\n");
                sb.append("   Creador: ").append(inc.getString("creator")).append("\n");
                sb.append("   Data: ").append(inc.getString("detected_at"), 0, 10).append("\n\n");
            }
            return sb.toString();

        } catch (Exception e) {
            return "Error parsejant JSON: " + e.getMessage() + "\n\nJSON rebut:\n" + jsonStr;
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        executor.shutdown();
    }
}
