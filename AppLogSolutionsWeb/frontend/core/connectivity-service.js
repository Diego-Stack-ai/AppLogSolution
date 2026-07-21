// connectivity-service.js
import { db } from "./firebase-init.js?v=6.194";

class ConnectivityService {
    constructor() {
        this.status = navigator.onLine ? 'online' : 'offline';
        this.listeners = [];
        this.pingUrl = './favicon.ico'; // Usiamo la favicon locale per il ping
        this.pingInterval = 30000; // 30 secondi
        this.pingTimeout = 5000;   // 5 secondi timeout
        this.intervalId = null;

        this.init();
    }

    init() {
        window.addEventListener('online', () => this.handleNetworkChange(true));
        window.addEventListener('offline', () => this.handleNetworkChange(false));

        // Avvia il ping periodico se inizialmente online
        if (navigator.onLine) {
            this.startPingInterval();
        }
    }

    addEventListener(callback) {
        this.listeners.push(callback);
        // Notifica immediatamente dello stato attuale
        callback(this.status);
    }

    removeEventListener(callback) {
        this.listeners = this.listeners.filter(l => l !== callback);
    }

    async handleNetworkChange(isOnline) {
        if (!isOnline) {
            this.updateStatus('offline');
            this.stopPingInterval();
        } else {
            // Esegue un ping reale per accertarsi che la connessione sia attiva e non farlocca (es: captive portal)
            const actualOnline = await this.ping();
            this.updateStatus(actualOnline ? 'online' : 'unstable');
            this.startPingInterval();
        }
    }

    updateStatus(newStatus) {
        if (this.status !== newStatus) {
            console.log(`[ConnectivityService] Stato connessione cambiato in: ${newStatus.toUpperCase()}`);
            this.status = newStatus;
            this.notifyListeners();
        }
    }

    notifyListeners() {
        this.listeners.forEach(callback => {
            try {
                callback(this.status);
            } catch (e) {
                console.error("[ConnectivityService] Errore notifica listener:", e);
            }
        });
    }

    startPingInterval() {
        this.stopPingInterval();
        this.intervalId = setInterval(async () => {
            if (navigator.onLine) {
                const isOnline = await this.ping();
                this.updateStatus(isOnline ? 'online' : 'unstable');
            } else {
                this.updateStatus('offline');
            }
        }, this.pingInterval);
    }

    stopPingInterval() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    async ping() {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.pingTimeout);

            const response = await fetch(`${this.pingUrl}?t=${Date.now()}`, {
                method: 'HEAD',
                signal: controller.signal,
                cache: 'no-store'
            });

            clearTimeout(timeoutId);
            return response.ok;
        } catch (e) {
            console.warn("[ConnectivityService] Ping fallito (nessuna rotta internet o instabile):", e.message);
            return false;
        }
    }

    getStatus() {
        return this.status;
    }
}

export const connectivityService = new ConnectivityService();
