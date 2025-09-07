"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { 
  Brain, 
  Play, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Eye,
  RefreshCw,
  AlertCircle
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface AutomationStatusProps {
  videoId: string;
  onExecute?: () => void;
}

interface StatusData {
  video_id: string;
  analysis_status: string;
  analysis_steps: number;
  analysis_error?: string;
  execution_status: string;
  execution_log: string[];
  execution_error?: string;
  last_updated?: string;
}

export default function AutomationStatus({ videoId, onExecute }: AutomationStatusProps) {
  const [status, setStatus] = useState<StatusData | null>(null);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const { toast } = useToast();

  const fetchStatus = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:8000/api/automation/status/${videoId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setStatus(data.data);
      }
    } catch (error) {
      console.error("Failed to fetch status:", error);
    } finally {
      setLoading(false);
    }
  };

  const triggerExecution = async () => {
    if (!status || status.analysis_status !== 'completed') {
      toast.error("Video analysis must be completed first");
      return;
    }

    setExecuting(true);
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:8000/api/automation/trigger/${videoId}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.ok) {
        toast.success("Automation started!");
        onExecute?.();
        // Start polling for updates
        const interval = setInterval(() => {
          fetchStatus();
          if (status?.execution_status === 'completed' || status?.execution_status === 'failed') {
            clearInterval(interval);
          }
        }, 2000);
      } else {
        const error = await response.json();
        toast.error(error.message || "Failed to start automation");
      }
    } catch (error) {
      toast.error("Failed to start automation");
    } finally {
      setExecuting(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    
    // Poll for updates if processing
    const interval = setInterval(() => {
      if (status?.analysis_status === 'processing' || status?.execution_status === 'running') {
        fetchStatus();
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [videoId]);

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4 animate-spin" />
            <span>Loading automation status...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!status) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-muted-foreground">
            <AlertCircle className="h-8 w-8 mx-auto mb-2" />
            <p>No automation data available</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getStatusIcon = (statusType: string) => {
    switch (statusType) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />;
      case 'running':
      case 'processing':
        return <RefreshCw className="h-4 w-4 animate-spin text-blue-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusBadge = (statusType: string) => {
    const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
      'completed': 'default',
      'failed': 'destructive',
      'running': 'secondary',
      'processing': 'secondary',
      'not_started': 'outline'
    };
    
    return (
      <Badge variant={variants[statusType] || 'outline'}>
        {statusType.replace('_', ' ')}
      </Badge>
    );
  };

  return (
    <div className="space-y-4">
      {/* Analysis Status */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-lg">
            <Brain className="h-5 w-5" />
            Video Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              {getStatusIcon(status.analysis_status)}
              <span className="font-medium">Analysis Status</span>
            </div>
            {getStatusBadge(status.analysis_status)}
          </div>
          
          {status.analysis_status === 'completed' && (
            <div className="text-sm text-muted-foreground">
              ✅ Extracted {status.analysis_steps} automation steps
            </div>
          )}
          
          {status.analysis_error && (
            <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
              <strong>Error:</strong> {status.analysis_error}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Execution Status */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-lg">
            <Play className="h-5 w-5" />
            Browser Automation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              {getStatusIcon(status.execution_status)}
              <span className="font-medium">Execution Status</span>
            </div>
            {getStatusBadge(status.execution_status)}
          </div>

          {status.analysis_status === 'completed' && status.execution_status === 'not_started' && (
            <Button 
              onClick={triggerExecution} 
              disabled={executing}
              className="w-full"
            >
              {executing ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Starting Automation...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4 mr-2" />
                  Start Browser Automation
                </>
              )}
            </Button>
          )}

          {status.execution_log.length > 0 && (
            <div className="mt-3">
              <h4 className="text-sm font-medium mb-2">Execution Log:</h4>
              <div className="bg-gray-50 p-2 rounded text-xs font-mono max-h-32 overflow-y-auto">
                {status.execution_log.map((log, index) => (
                  <div key={index}>{log}</div>
                ))}
              </div>
            </div>
          )}

          {status.execution_error && (
            <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
              <strong>Error:</strong> {status.execution_error}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Refresh Button */}
      <Button 
        variant="outline" 
        onClick={fetchStatus}
        className="w-full"
      >
        <RefreshCw className="h-4 w-4 mr-2" />
        Refresh Status
      </Button>
    </div>
  );
}