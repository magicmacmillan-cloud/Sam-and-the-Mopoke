package com.msa.freedoom;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.SharedPreferences;
import android.content.Context;
import android.content.res.Resources;
import android.net.Uri;

import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class CrashActivity extends Activity {
    private Uri downloadUri;
    private File engineLog;
    private String baseHeader;
    private final Object writeLock = new Object();
    private volatile String stage = "Crash logger starting.";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        File ext = getExternalFilesDir(null);
        engineLog = new File(ext, "Freedoom/config/z");

        SharedPreferences prefs = getSharedPreferences("MOPOKE_CRASH", MODE_PRIVATE);
        int seq = prefs.getInt("seq", 0) + 1;
        prefs.edit().putInt("seq", seq).apply();

        String fileName = String.format(Locale.US, "Mopoke Crash %03d.txt", seq);
        downloadUri = createDownload(fileName);
        baseHeader =
            "Zombie Mopoke crash diagnostic\n" +
            "File: " + fileName + "\n" +
            "Package: " + getPackageName() + "\n" +
            "Engine log: " + engineLog.getAbsolutePath() + "\n\n";

        try {
            if (engineLog.exists()) engineLog.delete();
        } catch (Throwable ignored) {}

        final Thread.UncaughtExceptionHandler previous = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> {
            StringWriter sw = new StringWriter();
            error.printStackTrace(new PrintWriter(sw));
            writeSnapshot(
                "JAVA UNCAUGHT EXCEPTION\n" +
                "Stage: " + stage + "\n" +
                "Thread: " + thread.getName() + "\n" +
                sw.toString() + "\n"
            );
            if (previous != null) previous.uncaughtException(thread, error);
        });

        stage = "Android launcher alive.";
        writeSnapshot(stage + "\n");

        Thread sync = new Thread(() -> {
            for (int i = 0; i < 2400; i++) {
                try {
                    writeSnapshot("Stage: " + stage + "\nDiagnostic sync active.\n");
                    Thread.sleep(250);
                } catch (Throwable ignored) {
                    return;
                }
            }
        }, "MopokeCrashSync");
        sync.setDaemon(true);
        sync.start();

        try {
            launchDoomDirectly();
        } catch (Throwable t) {
            StringWriter sw = new StringWriter();
            t.printStackTrace(new PrintWriter(sw));
            writeSnapshot(
                "FAILED BEFORE DOOM WINDOW OPENED\n" +
                "Stage: " + stage + "\n" +
                sw.toString()
            );
            throw new RuntimeException(t);
        }
    }

    private void launchDoomDirectly() throws Exception {
        Context app = getApplication();

        stage = "Loading Doom Android settings.";
        writeSnapshot("Stage: " + stage + "\n");
        Class<?> appSettings = Class.forName("com.msa.freedoom.AppSettings");
        Method reloadSettings = appSettings.getMethod("reloadSettings", Context.class);
        Method resetBaseDir = appSettings.getMethod("resetBaseDir", Context.class);
        Method createDirectories = appSettings.getMethod("createDirectories", Context.class);
        Method getQuakeFullDir = appSettings.getMethod("getQuakeFullDir");
        Method getIntOption = appSettings.getMethod("getIntOption", Context.class, String.class, int.class);

        reloadSettings.invoke(null, app);
        resetBaseDir.invoke(null, app);

        stage = "Creating Doom data directories.";
        writeSnapshot("Stage: " + stage + "\n");
        createDirectories.invoke(null, app);
        String base = (String) getQuakeFullDir.invoke(null);

        engineLog = new File(base, "z");
        try {
            if (engineLog.exists()) engineLog.delete();
        } catch (Throwable ignored) {}

        stage = "Installing bundled Doom engine/game assets.";
        writeSnapshot("Stage: " + stage + "\n");
        Class<?> utils = Class.forName("com.msa.freedoom.Utils");
        Method copyAsset = utils.getMethod("copyAsset", Context.class, String.class, String.class);

        String[] baseAssets = {
            "sam-and-the-mopoke.wad",
            "game_widescreen_gfx.pk3",
            "lights.pk3",
            "brightmaps.pk3",
            "gzdoom.sf2"
        };
        for (String asset : baseAssets) {
            stage = "Copying " + asset;
            writeSnapshot("Stage: " + stage + "\n");
            copyAsset.invoke(null, this, asset, base);
        }

        String res = base + "/res";
        String[] resAssets = {"uzdoom.pk3", "uzdoom_game_support.pk3"};
        for (String asset : resAssets) {
            stage = "Copying " + asset;
            writeSnapshot("Stage: " + stage + "\n");
            copyAsset.invoke(null, this, asset, res);
        }
        stage = "Copying soundfont.";
        writeSnapshot("Stage: " + stage + "\n");
        copyAsset.invoke(null, this, "gzdoom.sf2", base + "/soundfonts");

        stage = "Initialising Android controller map.";
        writeSnapshot("Stage: " + stage + "\n");
        Method getGameGamepadConfig = utils.getMethod("getGameGamepadConfig", Resources.class);
        Object actions = getGameGamepadConfig.invoke(null, getResources());
        Class<?> gamePadFragment = Class.forName("com.beloko.touchcontrols.GamePadFragment");
        Field gamepadActions = gamePadFragment.getField("gamepadActions");
        gamepadActions.set(null, actions);

        int resDiv = (Integer) getIntOption.invoke(null, this, "gzdoom_res_div", 1);

        stage = "Starting GZDoom native activity.";
        writeSnapshot("Stage: " + stage + "\n");

        Intent intent = new Intent();
        intent.setComponent(new ComponentName(this, "com.msa.freedoom.Game"));
        intent.setAction(Intent.ACTION_MAIN);
        intent.putExtra("res_div", resDiv);
        intent.putExtra("game_path", base);
        intent.putExtra("game", "com.samandthemopoke.game");
        intent.putExtra("args", "-iwad sam-and-the-mopoke.wad -logfile z +map MAP01");
        startActivity(intent);

        stage = "GZDoom activity launched.";
        writeSnapshot("Stage: " + stage + "\n");
        finish();
    }

    private Uri createDownload(String fileName) {
        try {
            ContentValues values = new ContentValues();
            values.put("_display_name", fileName);
            values.put("mime_type", "text/plain");
            values.put("relative_path", "Download/");
            return getContentResolver().insert(
                Uri.parse("content://media/external/downloads"), values
            );
        } catch (Throwable t) {
            return null;
        }
    }

    private void writeSnapshot(String status) {
        synchronized (writeLock) {
            if (downloadUri == null) return;
            OutputStream out = null;
            try {
                ContentResolver resolver = getContentResolver();
                out = resolver.openOutputStream(downloadUri, "wt");
                if (out == null) return;

                out.write(baseHeader.getBytes(StandardCharsets.UTF_8));
                out.write(status.getBytes(StandardCharsets.UTF_8));

                if (engineLog.exists()) {
                    out.write("\n--- GZDoom log ---\n".getBytes(StandardCharsets.UTF_8));
                    FileInputStream in = new FileInputStream(engineLog);
                    byte[] buf = new byte[32768];
                    int n;
                    while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
                    in.close();
                } else {
                    out.write("\nNo GZDoom log file exists yet.\n".getBytes(StandardCharsets.UTF_8));
                }
                out.flush();
            } catch (Throwable ignored) {
            } finally {
                if (out != null) {
                    try { out.close(); } catch (Throwable ignored) {}
                }
            }
        }
    }
}
