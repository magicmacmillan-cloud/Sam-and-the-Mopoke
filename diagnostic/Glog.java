package com.msa.freedoom;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;

import org.libsdl.app2012.SDLActivity;

import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class Glog extends SDLActivity {
    private Uri crashUri;
    private int crashSeq;

    @Override
    protected String[] getLibraries() {
        return new String[] {
            "hidapi",
            "saffal",
            "openal",
            "zmusic_uz",
            "touchcontrols",
            "SDL2",
            "uzdoom"
        };
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        Intent i = getIntent();
        crashSeq = i != null ? i.getIntExtra("mopoke_crash_seq", 0) : 0;
        String uri = i != null ? i.getStringExtra("mopoke_crash_uri") : null;
        if (uri != null) {
            try { crashUri = Uri.parse(uri); } catch (Throwable ignored) {}
        }

        final Thread.UncaughtExceptionHandler previous =
            Thread.getDefaultUncaughtExceptionHandler();

        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> {
            StringWriter sw = new StringWriter();
            error.printStackTrace(new PrintWriter(sw));
            appendCrash(
                "\n\n--- GAME PROCESS JAVA CRASH ---\n" +
                "Process: " + getPackageName() + ":Game\n" +
                "Thread: " + thread.getName() + "\n" +
                "Exception: " + error.toString() + "\n\n" +
                sw.toString() + "\n"
            );
            if (previous != null) {
                previous.uncaughtException(thread, error);
            }
        });

        appendCrash("\n--- Game process started; entering SDLActivity.onCreate ---\n");
        super.onCreate(savedInstanceState);
        appendCrash("\n--- SDLActivity.onCreate returned ---\n");
    }

    private void appendCrash(String text) {
        if (crashUri != null) {
            try {
                OutputStream out = getContentResolver().openOutputStream(crashUri, "wa");
                if (out != null) {
                    out.write(text.getBytes(StandardCharsets.UTF_8));
                    out.flush();
                    out.close();
                    return;
                }
            } catch (Throwable ignored) {}
        }

        try {
            String name = String.format(Locale.US, "Mopoke Crash Game %03d.txt",
                crashSeq > 0 ? crashSeq : 1);
            ContentValues v = new ContentValues();
            v.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
            v.put(MediaStore.MediaColumns.MIME_TYPE, "text/plain");
            v.put(MediaStore.MediaColumns.RELATIVE_PATH, "Download/");
            Uri u = getContentResolver().insert(
                MediaStore.Downloads.EXTERNAL_CONTENT_URI, v);
            if (u != null) {
                OutputStream out = getContentResolver().openOutputStream(u, "wt");
                if (out != null) {
                    out.write(text.getBytes(StandardCharsets.UTF_8));
                    out.flush();
                    out.close();
                }
            }
        } catch (Throwable ignored) {}
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        System.exit(0);
    }
}
