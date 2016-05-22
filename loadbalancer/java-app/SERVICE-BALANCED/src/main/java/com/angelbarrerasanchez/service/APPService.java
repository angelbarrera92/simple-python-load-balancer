package com.angelbarrerasanchez.service;
import static spark.Spark.get;
import static spark.Spark.ipAddress;
import static spark.Spark.port;

import java.net.InetAddress;
import java.net.UnknownHostException;

import org.json.JSONException;
import org.json.JSONObject;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;

public class APPService {
	
	private static int myPort = 8080;
	
	private static String myEmail = "angel@angel.com";
	private static String myPass = "123456";
	private static String myMicroServiceName = "MyMicroservice";
	private static String loadBalancerHost = "localhost";
	
	public static void main(String[] args) throws UnirestException, JSONException, UnknownHostException, InterruptedException {
		System.out.println("WAITTING FOR MONGODB");
		Thread.sleep(15000); //WAIT TO MONGODB 15s
		System.out.println("WAITTED FOR MONGODB");
		
		//SERVER CONF
		if(System.getenv("myPort")!=null){
			myPort = Integer.valueOf(System.getenv("myPort"));
		}
		ipAddress(InetAddress.getLocalHost().getHostAddress());
		port(myPort);
        
        //ENDPOINTS
        get("/status", (req, res) -> "I AM OK");
        get("/", (req, res) -> "I am " + InetAddress.getLocalHost().getHostAddress() + ":" + myPort);
        get("/hello/:name", (req, res) -> {
		    return "Hello " + req.params(":name") + "! (From " + InetAddress.getLocalHost().getHostAddress() + ":" + myPort + ")";
		});
        
        //REGISTER INTO BALANCER
        registerAppInBalancer("/status");
	}
	
	private static void registerAppInBalancer(final String myStatusUri) throws UnirestException, JSONException, UnknownHostException{
		JSONObject json = new JSONObject();
		json.put("email", myEmail);
		json.put("password", myPass);
		
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
		
		String token = (String) jsonResponse.getBody().getObject().get("access_token");
		
		json = new JSONObject();
		json.put("host", InetAddress.getLocalHost().getHostAddress());
		json.put("port", myPort);
		json.put("statuspath", myStatusUri);
		
		Unirest.post("http://"+loadBalancerHost+":5000/api/nodes/" + myMicroServiceName)
				  .header("accept", "application/json")
				  .header("Content-Type", "application/json")
				  .header("Authorization", "JWT " + token)
				  .body(json)
				  .asString();
	}

}
