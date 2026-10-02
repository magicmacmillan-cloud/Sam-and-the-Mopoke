package com.msa.freedoom;

import android.app.Activity;
import android.app.ActivityManager;
import android.app.ApplicationExitInfo;
import android.os.Build;
import android.os.Bundle;
import android.content.Intent;
import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.SharedPreferences;
import android.content.Context;
import android.content.res.Resources;
import android.net.Uri;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class CrashActivity extends Activity {
    private Uri downloadUri;
    private File engineLog;
    private String baseHeader;
    private String previousExitReport = "";
    private final Object writeLock = new Object();
    private volatile String stage = "Crash logger starting.";
    private int crashSeq = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        File ext = getExternalFilesDir(null);
        engineLog = new File(ext, "Freedoom/config/user_files/gzdoom_log.txt");

        SharedPreferences prefs = getSharedPreferences("MOPOKE_CRASH", MODE_PRIVATE);
        int seq = prefs.getInt("seq", 0) + 1;
        prefs.edit().putInt("seq", seq).apply();

        String fileName = String.format(Locale.US, "Mopoke Crash %03d.txt", seq);
        downloadUri = createDownload(fileName);

        previousExitReport = buildPreviousExitReport();

        baseHeader =
            "Zombie Mopoke crash diagnostic\n" +
            "File: " + fileName + "\n" +
            "Package: " + getPackageName() + "\n" +
            "Device: " + Build.MANUFACTURER + " " + Build.MODEL + "\n" +
            "Android SDK: " + Build.VERSION.SDK_INT + "\n" +
            "ABI: " + (Build.SUPPORTED_ABIS.length > 0 ? Build.SUPPORTED_ABIS[0] : "unknown") + "\n" +
            "Engine log: " + engineLog.getAbsolutePath() + "\n\n" +
            previousExitReport;

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

        setStage("Android launcher alive.");
        writeSnapshot("Stage: " + stage + "\n");

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

    private String buildPreviousExitReport() {
        StringBuilder sb = new StringBuilder();
        sb.append("--- Previous Android process exit ---\n");
        if (Build.VERSION.SDK_INT < 30) {
            sb.append("ApplicationExitInfo unavailable below Android 11.\n\n");
            return sb.toString();
        }

        try {
            ActivityManager am = (ActivityManager) getSystemService(ACTIVITY_SERVICE);
            List<ApplicationExitInfo> exits =
                am.getHistoricalProcessExitReasons(getPackageName(), 0, 5);

            if (exits == null || exits.isEmpty()) {
                sb.append("No previous process exit record available.\n\n");
                return sb.toString();
            }

            int index = 0;
            for (ApplicationExitInfo e : exits) {
                sb.append("\nExit record #").append(++index).append("\n");
                sb.append("Process: ").append(e.getProcessName()).append("\n");
                sb.append("Reason: ").append(reasonName(e.getReason()))
                  .append(" (").append(e.getReason()).append(")\n");
                sb.append("Status: ").append(e.getStatus()).append("\n");
                sb.append("Importance: ").append(e.getImportance()).append("\n");
                sb.append("Timestamp: ")
                  .append(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.US)
                  .format(new Date(e.getTimestamp()))).append("\n");
                sb.append("Description: ").append(String.valueOf(e.getDescription())).append("\n");
                sb.append("PSS KB: ").append(e.getPss()).append("\n");
                sb.append("RSS KB: ").append(e.getRss()).append("\n");

                byte[] summary = e.getProcessStateSummary();
                if (summary != null && summary.length > 0) {
                    sb.append("Last saved app stage: ")
                      .append(new String(summary, StandardCharsets.UTF_8)).append("\n");
                }

                try {
                    InputStream trace = e.getTraceInputStream();
                    if (trace != null) {
                        byte[] traceBytes = readLimited(trace, 1024 * 1024);
                        trace.close();
                        sb.append("--- Android exit trace / tombstone ---\n");
                        sb.append(new String(traceBytes, StandardCharsets.UTF_8));
                        if (traceBytes.length > 0 && traceBytes[traceBytes.length - 1] != '\n') {
                            sb.append("\n");
                        }
                    } else {
                        sb.append("Android exit trace: unavailable.\n");
                    }
                } catch (Throwable traceError) {
                    sb.append("Android exit trace read failed: ")
                      .append(traceError.toString()).append("\n");
                }
            }
        } catch (Throwable t) {
            sb.append("Previous exit query failed: ").append(t.toString()).append("\n");
        }
        sb.append("\n");
        return sb.toString();
    }

    private byte[] readLimited(InputStream in, int max) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buf = new byte[16384];
        int total = 0;
        while (total < max) {
            int want = Math.min(buf.length, max - total);
            int n = in.read(buf, 0, want);
            if (n <= 0) break;
            out.write(buf, 0, n);
            total += n;
        }
        return out.toByteArray();
    }

    private String reasonName(int reason) {
        switch (reason) {
            case ApplicationExitInfo.REASON_EXIT_SELF: return "EXIT_SELF";
            case ApplicationExitInfo.REASON_SIGNALED: return "SIGNALED";
            case ApplicationExitInfo.REASON_LOW_MEMORY: return "LOW_MEMORY";
            case ApplicationExitInfo.REASON_CRASH: return "CRASH_JAVA";
            case ApplicationExitInfo.REASON_CRASH_NATIVE: return "CRASH_NATIVE";
            case ApplicationExitInfo.REASON_ANR: return "ANR";
            case ApplicationExitInfo.REASON_INITIALIZATION_FAILURE: return "INITIALIZATION_FAILURE";
            case ApplicationExitInfo.REASON_PERMISSION_CHANGE: return "PERMISSION_CHANGE";
            case ApplicationExitInfo.REASON_EXCESSIVE_RESOURCE_USAGE: return "EXCESSIVE_RESOURCE_USAGE";
            case ApplicationExitInfo.REASON_USER_REQUESTED: return "USER_REQUESTED";
            case ApplicationExitInfo.REASON_USER_STOPPED: return "USER_STOPPED";
            case ApplicationExitInfo.REASON_DEPENDENCY_DIED: return "DEPENDENCY_DIED";
            case ApplicationExitInfo.REASON_OTHER: return "OTHER";
            default: return "UNKNOWN";
        }
    }

    private void setStage(String s) {
        stage = s;
        if (Build.VERSION.SDK_INT >= 30) {
            try {
                ActivityManager am = (ActivityManager) getSystemService(ACTIVITY_SERVICE);
                am.setProcessStateSummary(("stage=" + s).getBytes(StandardCharsets.UTF_8));
            } catch (Throwable ignored) {}
        }
    }

    private void launchDoomDirectly() throws Exception {
        Context app = getApplication();

        setStage("Loading Doom Android settings.");
        writeSnapshot("Stage: " + stage + "\n");
        Class<?> appSettings = Class.forName("com.msa.freedoom.AppSettings");
        Method reloadSettings = appSettings.getMethod("reloadSettings", Context.class);
        Method resetBaseDir = appSettings.getMethod("resetBaseDir", Context.class);
        Method createDirectories = appSettings.getMethod("createDirectories", Context.class);
        Method getQuakeFullDir = appSettings.getMethod("getQuakeFullDir");
        Method getIntOption = appSettings.getMethod("getIntOption", Context.class, String.class, int.class);

        reloadSettings.invoke(null, app);
        resetBaseDir.invoke(null, app);

        setStage("Creating Doom data directories.");
        writeSnapshot("Stage: " + stage + "\n");
        createDirectories.invoke(null, app);
        String base = (String) getQuakeFullDir.invoke(null);

        engineLog = new File(base, "user_files/gzdoom_log.txt");
        try {
            if (engineLog.exists()) engineLog.delete();
        } catch (Throwable ignored) {}

        setStage("Installing bundled Doom engine/game assets.");
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
            setStage("Copying " + asset);
            writeSnapshot("Stage: " + stage + "\n");
            copyAsset.invoke(null, this, asset, base);
        }

        String res = base + "/res";
        String[] resAssets = {"uzdoom.pk3", "uzdoom_game_support.pk3"};
        for (String asset : resAssets) {
            setStage("Copying " + asset);
            writeSnapshot("Stage: " + stage + "\n");
            copyAsset.invoke(null, this, asset, res);
        }
        setStage("Copying soundfont.");
        writeSnapshot("Stage: " + stage + "\n");
        copyAsset.invoke(null, this, "gzdoom.sf2", base + "/soundfonts");

        setStage("Initialising Android controller map.");
        writeSnapshot("Stage: " + stage + "\n");
        Method getGameGamepadConfig = utils.getMethod("getGameGamepadConfig", Resources.class);
        Object actions = getGameGamepadConfig.invoke(null, getResources());
        Class<?> gamePadFragment = Class.forName("com.beloko.touchcontrols.GamePadFragment");
        Field gamepadActions = gamePadFragment.getField("gamepadActions");
        gamepadActions.set(null, actions);

        int resDiv = (Integer) getIntOption.invoke(null, this, "gzdoom_res_div", 1);

        setStage("Starting GZDoom native activity.");
        writeSnapshot("Stage: " + stage + "\n");

        Intent intent = new Intent();
        intent.setComponent(new ComponentName(this, "com.msa.freedoom.Glog"));
        intent.setAction(Intent.ACTION_MAIN);
        intent.putExtra("res_div", resDiv);
        intent.putExtra("game_path", base);
        intent.putExtra("game", "com.msa.freedoom");
        intent.putExtra("args", "-iwad sam-and-the-mopoke.wad +map MAP01");
        if (downloadUri != null) intent.putExtra("mopoke_crash_uri", downloadUri.toString());
        intent.putExtra("mopoke_crash_seq", crashSeq);
        startActivity(intent);

        setStage("GZDoom activity launched.");
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
