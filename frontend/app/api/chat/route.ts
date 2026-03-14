import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, user, conversationHistory } = body;

    let endpoint = process.env.ML_MODEL_ENDPOINT || 
                   process.env.NEXT_PUBLIC_ML_BACKEND || 
                   process.env.NEXT_API_URL;
    
    if (!endpoint) {
      console.error("Missing Backend URL environment variable (checked ML_MODEL_ENDPOINT, NEXT_PUBLIC_ML_BACKEND, NEXT_API_URL)");
      return NextResponse.json(
        { error: "Server configuration error: Backend URL is missing" },
        { status: 500 }
      );
    }

    // Ensure it's the full API path
    if (!endpoint.endsWith('/api/chat')) {
      endpoint = `${endpoint.replace(/\/$/, '')}/api/chat`;
    }

    console.log(`Forwarding chat request to: ${endpoint}`);

    // Call your ML model
    try {
      const mlResponse = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(process.env.ML_MODEL_API_KEY && {
            Authorization: `Bearer ${process.env.ML_MODEL_API_KEY}`,
          }),
        },
        body: JSON.stringify({
          query: message,
          user: user,
          history: conversationHistory || [],
        }),
      });

      if (!mlResponse.ok) {
        const errorText = await mlResponse.text();
        console.error(`ML Model Error (${mlResponse.status}): ${errorText}`);
        return NextResponse.json(
          { error: `Backend returned error: ${mlResponse.status}` },
          { status: mlResponse.status }
        );
      }

      const mlData = await mlResponse.json();

      return NextResponse.json({
        reply: mlData.reply || mlData.response || mlData.answer,
        metadata: mlData.metadata || {},
        confidence: mlData.confidence,
      });
    } catch (fetchError: any) {
      console.error("Fetch error while calling ML model:", fetchError);
      return NextResponse.json(
        { error: `Failed to connect to backend: ${fetchError.message}` },
        { status: 502 }
      );
    }
  } catch (error: any) {
    console.error("Chat API Request Error:", error);
    return NextResponse.json(
      { error: "Failed to process message request" },
      { status: 400 },
    );
  }
}
