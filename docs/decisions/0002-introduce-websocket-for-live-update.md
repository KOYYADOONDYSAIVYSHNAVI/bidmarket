# <!-- Introduce WebSocket for live update of auction items -->

## Context and Problem Statement

When browsing the auction website, it is not user-friendly for users to refresh the page and get updates on the auction items. Instead, a mechanism that allows users keep tracking the items they are interested in without manual intervention should be implemented.


## Decision Outcome

WebSocket allows server and client (browser) maintains a connection. Both side can send/ receive data. There is basically no other options since WebSocket is the only protocol that browsers support that allows this type of use cases. Thus, Websocket interfaces will be implemented at both server and client side to allow a better user experience.
