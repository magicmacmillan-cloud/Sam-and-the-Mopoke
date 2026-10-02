package com.msa.freedoom;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.SharedPreferences;
import android.net.Uri;

import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class CrashActivity extends Activity {
    private Uri downloadUri;
    private File engineLog;
    private String baseHeader;
    private final Object writeLock = new Object();

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

        writeSnapshot("Launcher started. Waiting for Doom/GZDoom output...\n");

        final Thread.UncaughtExceptionHandler previous = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> {
            StringWriter sw = new StringWriter();
            error.printStackTrace(new PrintWriter(sw));
            writeSnapshot(
                "JAVA UNCAUGHT EXCEPTION\n" +
                "Thread: " + thread.getName() + "\n" +
                sw.toString() + "\n"
            );
            if (previous != null) {
                previous.uncaughtException(thread, error);
            }
        });

        Thread sync = new Thread(() -> {
            for (int i = 0; i < 2400; i++) {
                try {
                    writeSnapshot("Doom process launched. Diagnostic sync active.\n");
                    Thread.sleep(250);
                } catch (Throwable ignored) {
                    return;
                }
            }
        }, "MopokeCrashSync");
        sync.setDaemon(true);
        sync.start();

        try {
            Intent intent = new Intent();
            intent.setComponent(new ComponentName(this, "com.msa.freedoom.EntryActivity"));
            intent.setAction(Intent.ACTION_MAIN);
            startActivity(intent);
            finish();
        } catch (Throwable t) {
            StringWriter sw = new StringWriter();
            t.printStackTrace(new PrintWriter(sw));
            writeSnapshot("FAILED TO START ENTRY ACTIVITY\n" + sw.toString());
            throw t;
        }
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
