use reqwest::blocking::Client;
use reqwest::StatusCode;
//use scraper::{Html, Selector};

fn main() -> Result<(), Box<dyn std::error::Error>>{
	let client = Client::new();
	let mut res = client.get("https://verify.bmdc.org.bd")
					.send()?;
	match res.status() {
		StatusCode::OK => println!("Connected with Rust!"),
		s => println!("Received response status: {s:?}"),
	};

	Ok(())
}
