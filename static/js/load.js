function load(callbacks) {
    window.onload = () => {
        for (i = 0 ; i < callbacks.length ; i++) {
            callbacks[i]();
        }
    }
}