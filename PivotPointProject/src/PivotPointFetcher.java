package PivotPointProject.src;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import org.json.JSONObject;

public class PivotPointFetcher {

    private static String fetchData(String pairId, String timeFrame) throws Exception {
        String urlString = "https://api.yourdatasource.com/data?pair_id=" + pairId + "&time_frame=" + timeFrame;
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        StringBuilder content;
        try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            String inputLine;
            content = new StringBuilder();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
        }
        conn.disconnect();

        return content.toString();
    }

    private static void parseAndDisplayData(String jsonData) {
        JSONObject jsonObject = new JSONObject(jsonData);  // Create JSONObject from jsonData
        String s1 = jsonObject.optString("S1", "None");
        String s2 = jsonObject.optString("S2", "None");
        String s3 = jsonObject.optString("S3", "None");
        String pivot = jsonObject.optString("Pivot", "None");
        String r1 = jsonObject.optString("R1", "None");
        String r2 = jsonObject.optString("R2", "None");
        String r3 = jsonObject.optString("R3", "None");

        System.out.println("S1: " + s1);
        System.out.println("S2: " + s2);
        System.out.println("S3: " + s3);
        System.out.println("Pivot: " + pivot);
        System.out.println("R1: " + r1);
        System.out.println("R2: " + r2);
        System.out.println("R3: " + r3);
    }

    public static void main(String[] args) {
        try {
            String pairId = "1";
            String timeFrame = "3600";
            String jsonData = fetchData(pairId, timeFrame);
            parseAndDisplayData(jsonData);
        } catch (Exception e) {
            e.printStackTrace();  // Print the exception stack trace to help debug any issues
        }
    }
}
