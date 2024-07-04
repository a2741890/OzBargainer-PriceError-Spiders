# OzBargainer Price Error Crawler
> OzBargain is Australia's bargain hunting community, where hot deals, coupon codes, vouchers, special promotions and freebies are shared.
This web crawler aims to find posts containing keywords like "price error", "listing error", and send the email to infrom users about the deals.

## Usage
```python
python3 ./routine.py
```

## Example
The project is built by using Scrapy and uploaded to AWS EC2 instance (Ubuntu).
By using Screen (terminal multiplexer), the spider runs every 5 minutes on the cloud even the local ssh connection is terminated.  
https://github.com/a2741890/OzBargainer-PriceError-Spiders/blob/main/bash1.png
![alt text](https://github.com/a2741890/OzBargainer-PriceError-Spiders/blob/main/bash1.png)  
![alt text](https://github.com/a2741890/OzBargainer-PriceError-Spiders/blob/main/bash2.png)  
  
  
  
![alt text](https://github.com/a2741890/OzBargainer-PriceError-Spiders/blob/main/gmail1.PNG)  
  
  
  
The keywords will be highlighted with \_\_\_keyword___  
![alt text](https://github.com/a2741890/OzBargainer-PriceError-Spiders/blob/main/gmail2.PNG)  


