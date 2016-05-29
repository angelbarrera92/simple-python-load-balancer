package main.java.springmongodbdatarest;

import java.net.InetAddress;
import java.net.URISyntaxException;
import java.net.UnknownHostException;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.client.RestClientException;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;

@SpringBootApplication
public class Application {

	public static void main(String[] args) throws RestClientException, JSONException, UnknownHostException, URISyntaxException, UnirestException {
		SpringApplication.run(Application.class, args);
		registerInLoadBalancer();
	}

	private static void registerInLoadBalancer() throws RestClientException, URISyntaxException, JSONException, UnknownHostException, UnirestException {
		
		JSONObject json = new JSONObject();
		json.put("email", "angel@angel.com");
		json.put("password", "123456");
		
		String loadBalancerHost = "127.0.0.1";
		
		if(System.getenv("loadBalancerHost")!=null){
			loadBalancerHost = System.getenv("loadBalancerHost");
		}
		
		Unirest.post("http://"+loadBalancerHost+":5000/api/users")
				  .header("accept", "application/json")
				  .header("Content-Type", "application/json")
				  .body(json)
				  .asJson();
		
		HttpResponse<JsonNode> jsonResponse = Unirest.post("http://"+loadBalancerHost+":5000/api/auth")
				  .header("accept", "application/json")
				  .header("Content-Type", "application/json")
				  .body(json)
				  .asJson();
		
		final String token = (String) jsonResponse.getBody().getObject().get("access_token");
		
		Integer port = 8091;
		if(System.getenv("server.port")!=null){
			port = Integer.valueOf(System.getenv("server.port"));
		}
		
		json = new JSONObject();
		json.put("host", InetAddress.getLocalHost().getHostAddress());
		json.put("port", port);
		
		json.put("statuspath", "/health");
		
		String myMicroServiceName = "restproducts";
		
		Unirest.post("http://"+loadBalancerHost+":5000/api/nodes/" + myMicroServiceName)
				  .header("accept", "application/json")
				  .header("Content-Type", "application/json")
				  .header("Authorization", "JWT " + token)
				  .body(json)
				  .asString();
	}
}