<?php
if (isset($_POST['data'])) {
    $data = $_POST['data'];
    // Process the received data as needed
    // For example, you can save it to a file or send it to the JavaScript file via WebSocket or other methods.
    file_put_contents('./data/received_data.txt', $data . "\n", FILE_APPEND);
}
