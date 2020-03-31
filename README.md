# bridgedb-audio-captcha
Trial integration of audio captchas into bridgeDB's captcha page.

This project borrows elements from [BridgeDB's](https://bridges.torproject.org/) implementations of [Twisted](https://twistedmatrix.com/trac/) Resources to recreate its captcha page. Audio captchas 
were added with [this](https://github.com/lepture/captcha) library.

The project is a first step in coming up with a solution to [this](https://trac.torproject.org/projects/tor/ticket/10831) BridgeDB ticket.

A concern :
Given the simple input-output nature of the Python audio captcha library, it seems like it wouldn't take long to train a simple model to
accurately crack the audio captcha.

