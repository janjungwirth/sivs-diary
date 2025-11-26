# How to claim a free DNS name

For the assigment you will need a valid public DNS name

The service https://www.freemyip.com/main allows you to create single DNS entries on the domain freemyip.com.

1. Go to https://www.freemyip.com/main
2. Enter a DNS name and verify if it is still free (if not find another one)
3. If it is free claim it. You will see a Link to update the IP
4. Run on your server `curl https://freemyip.com/update?token=xxxxxxxxxxxxxxxxx&domain=yyyyyy.freemyip.com` (you will see a Link)
5. Enjoy your DNS name

You can also request Let's encrypt Certificates with the valid DNS server.  