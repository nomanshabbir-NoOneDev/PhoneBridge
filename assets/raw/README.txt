Put your raw Android screenshots here (png or jpg), named exactly:

  donor-bridge        Donor phone: Settings -> Donor bridge, running, with the addresses
  qr-setup            Donor phone: Settings -> iPhone & web companion, switched on, with the QR code
  companion-dialer    Companion phone: the dialer with the SIM choice
  incoming-call       Companion phone: the incoming call screen
  messages            Companion phone: Messages (inbox or a conversation)

Then run:  python3 tools/frame_screenshots.py
The framed pictures are written to assets/screens/. (The iPhone, iPad and computer pictures were made from the real web page.)
Hide real numbers, names and message text first.
