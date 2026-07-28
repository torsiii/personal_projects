package backend.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import backend.exception.ConfigLoadException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;

public final class ConfigManager {
    private static final Logger LOG = LoggerFactory.getLogger(ConfigManager.class);
    private static final AppConfig CONFIG = loadConfig();

    private ConfigManager() {
    }

    private static AppConfig loadConfig() {
        String profile = resolveProfile();
        String resourceName = "app-" + profile + ".json";

        LOG.info("Loading config: profile={}, resource={}", profile, resourceName);

        ClassLoader cl = Thread.currentThread().getContextClassLoader();

        try (InputStream in = cl.getResourceAsStream(resourceName)) {
            if (in == null) {
                throw new ConfigLoadException("Config not found: " + resourceName);
            }

            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(in, AppConfig.class);

        } catch (IOException e) {
            throw new ConfigLoadException("Failed to load config: " + resourceName, e);
        }
    }

    private static String resolveProfile() {
        String p = System.getProperty("app.profile");
        if (p != null && !p.isBlank()) {
            return p;
        }

        String env = System.getenv("APP_PROFILE");
        if (env != null && !env.isBlank()) {
            return env;
        }

        return "memory"; // default
    }

    public static AppConfig getConfig() {
        return CONFIG;
    }
}