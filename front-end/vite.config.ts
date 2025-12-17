import path from "path";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import fs from "fs";
import { exec } from "child_process";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");
  return {
    server: {
      port: 3000,
      host: "0.0.0.0",
    },
    plugins: [
      react(),
      {
        name: "rentalescrow-compile-endpoint",
        configureServer(server) {
          server.middlewares.use("/api/compile", async (req, res, next) => {
            if (req.method !== "GET" && req.method !== "POST") return next();

            const kontraktasDir = path.resolve(__dirname, "../kontraktas");
            const artifactPath = path.resolve(
              kontraktasDir,
              "build/contracts/RentalEscrow.json"
            );

            const sendArtifact = () => {
              try {
                const json = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
                const abi = json.abi;
                const bytecode = json.bytecode;
                res.setHeader("Content-Type", "application/json");
                res.end(JSON.stringify({ abi, bytecode }));
              } catch (e) {
                res.statusCode = 500;
                res.end(
                  JSON.stringify({
                    error: "Artifact not found or invalid",
                    details: String(e),
                  })
                );
              }
            };

            // Try to compile via Truffle; fallback to existing artifact if compile fails
            const cmd = "npx truffle compile";
            exec(cmd, { cwd: kontraktasDir }, (error, stdout, stderr) => {
              if (error) {
                // Fallback: try global truffle
                exec("truffle compile", { cwd: kontraktasDir }, (err2) => {
                  if (err2) {
                    // Last resort: return whatever artifact exists
                    sendArtifact();
                  } else {
                    sendArtifact();
                  }
                });
              } else {
                sendArtifact();
              }
            });
          });
        },
      },
    ],
    define: {
      "process.env.API_KEY": JSON.stringify(env.GEMINI_API_KEY),
      "process.env.GEMINI_API_KEY": JSON.stringify(env.GEMINI_API_KEY),
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "."),
      },
    },
  };
});
