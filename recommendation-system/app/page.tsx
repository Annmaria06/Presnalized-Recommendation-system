"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Play, Database, BarChart3, Star, TrendingUp, Brain, Target } from "lucide-react"

export default function RecommendationSystemDashboard() {
  const [activeStep, setActiveStep] = useState(0)
  const [isRunning, setIsRunning] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState(null)

  const steps = [
    {
      id: "collection",
      name: "Data Collection",
      icon: Database,
      description: "Download and prepare MovieLens dataset",
    },
    { id: "preprocessing", name: "Data Preprocessing", icon: BarChart3, description: "Clean and normalize the data" },
    { id: "eda", name: "Exploratory Analysis", icon: TrendingUp, description: "Analyze user-item interactions" },
    { id: "modeling", name: "Collaborative Filtering", icon: Brain, description: "Build recommendation models" },
  ]

  const runStep = async (stepIndex) => {
    setIsRunning(true)
    setProgress(0)

    // Simulate progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsRunning(false)
          setActiveStep(stepIndex + 1)
          return 100
        }
        return prev + 10
      })
    }, 500)
  }

  // Sample data for visualizations
  const ratingDistribution = [
    { rating: "1", count: 1200, percentage: 12 },
    { rating: "2", count: 1800, percentage: 18 },
    { rating: "3", count: 2500, percentage: 25 },
    { rating: "4", count: 3000, percentage: 30 },
    { rating: "5", count: 1500, percentage: 15 },
  ]

  const modelPerformance = [
    { model: "User-Based CF", rmse: 0.92, mae: 0.73, color: "#8884d8" },
    { model: "Item-Based CF", rmse: 0.89, mae: 0.71, color: "#82ca9d" },
  ]

  const datasetStats = {
    totalRatings: 100000,
    totalUsers: 943,
    totalItems: 1682,
    sparsity: 0.937,
    avgRating: 3.52,
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Recommendation System Project</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Complete implementation of collaborative filtering recommendation system with MovieLens dataset
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            {steps.map((step, index) => {
              const Icon = step.icon
              const isActive = index === activeStep
              const isCompleted = index < activeStep

              return (
                <div key={step.id} className="flex flex-col items-center">
                  <div
                    className={`
                    w-12 h-12 rounded-full flex items-center justify-center mb-2 transition-colors
                    ${
                      isCompleted
                        ? "bg-green-500 text-white"
                        : isActive
                          ? "bg-blue-500 text-white"
                          : "bg-gray-200 text-gray-500"
                    }
                  `}
                  >
                    <Icon className="w-6 h-6" />
                  </div>
                  <div className="text-center">
                    <div className="font-medium text-sm">{step.name}</div>
                    <div className="text-xs text-gray-500 max-w-24">{step.description}</div>
                  </div>
                </div>
              )
            })}
          </div>

          {isRunning && (
            <div className="mb-4">
              <Progress value={progress} className="w-full" />
              <p className="text-center text-sm text-gray-600 mt-2">
                Running {steps[activeStep]?.name}... {progress}%
              </p>
            </div>
          )}
        </div>

        <Tabs value={steps[activeStep]?.id || "collection"} className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            {steps.map((step, index) => (
              <TabsTrigger
                key={step.id}
                value={step.id}
                disabled={index > activeStep}
                className="flex items-center gap-2"
              >
                <step.icon className="w-4 h-4" />
                {step.name}
              </TabsTrigger>
            ))}
          </TabsList>

          {/* Data Collection Tab */}
          <TabsContent value="collection" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="w-5 h-5" />
                  Data Collection & Setup
                </CardTitle>
                <CardDescription>Download MovieLens 100K dataset and prepare for analysis</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Alert>
                  <AlertDescription>
                    This step will download the MovieLens 100K dataset containing 100,000 ratings from 943 users on
                    1,682 movies.
                  </AlertDescription>
                </Alert>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold text-blue-600">100K</div>
                      <div className="text-sm text-gray-600">Total Ratings</div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold text-green-600">943</div>
                      <div className="text-sm text-gray-600">Users</div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold text-purple-600">1,682</div>
                      <div className="text-sm text-gray-600">Movies</div>
                    </CardContent>
                  </Card>
                </div>

                <Button onClick={() => runStep(0)} disabled={isRunning} className="w-full">
                  <Play className="w-4 h-4 mr-2" />
                  {isRunning ? "Downloading Dataset..." : "Start Data Collection"}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Data Preprocessing Tab */}
          <TabsContent value="preprocessing" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  Data Preprocessing & Cleaning
                </CardTitle>
                <CardDescription>Clean data, handle missing values, and create user-item matrix</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium">Preprocessing Steps:</Label>
                    <ul className="text-sm text-gray-600 mt-2 space-y-1">
                      <li>• Remove missing values</li>
                      <li>• Filter users with {"<"} 5 ratings</li>
                      <li>• Filter items with {"<"} 5 ratings</li>
                      <li>• Create user-item matrix</li>
                      <li>• Normalize ratings by user mean</li>
                    </ul>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Expected Output:</Label>
                    <ul className="text-sm text-gray-600 mt-2 space-y-1">
                      <li>• Cleaned ratings dataset</li>
                      <li>• User-item interaction matrix</li>
                      <li>• User mean ratings</li>
                      <li>• Sparsity analysis</li>
                    </ul>
                  </div>
                </div>

                <Button onClick={() => runStep(1)} disabled={isRunning || activeStep < 1} className="w-full">
                  <Play className="w-4 h-4 mr-2" />
                  {isRunning ? "Processing Data..." : "Start Data Preprocessing"}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* EDA Tab */}
          <TabsContent value="eda" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Rating Distribution</CardTitle>
                  <CardDescription>Distribution of user ratings (1-5 scale)</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={ratingDistribution}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="rating" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Dataset Statistics</CardTitle>
                  <CardDescription>Key metrics from the dataset</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-blue-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">
                        {datasetStats.totalRatings.toLocaleString()}
                      </div>
                      <div className="text-sm text-gray-600">Total Ratings</div>
                    </div>
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">{datasetStats.avgRating}</div>
                      <div className="text-sm text-gray-600">Avg Rating</div>
                    </div>
                    <div className="text-center p-3 bg-purple-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">
                        {(datasetStats.sparsity * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-gray-600">Sparsity</div>
                    </div>
                    <div className="text-center p-3 bg-orange-50 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600">{datasetStats.totalUsers}</div>
                      <div className="text-sm text-gray-600">Active Users</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Exploratory Data Analysis
                </CardTitle>
                <CardDescription>Analyze user behavior and item popularity patterns</CardDescription>
              </CardHeader>
              <CardContent>
                <Button onClick={() => runStep(2)} disabled={isRunning || activeStep < 2} className="w-full">
                  <Play className="w-4 h-4 mr-2" />
                  {isRunning ? "Analyzing Data..." : "Start Exploratory Analysis"}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Modeling Tab */}
          <TabsContent value="modeling" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>User-Based Collaborative Filtering</CardTitle>
                  <CardDescription>Find similar users and recommend based on their preferences</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="text-sm text-gray-600">
                    <p>
                      <strong>Algorithm:</strong> Cosine similarity between users
                    </p>
                    <p>
                      <strong>Neighbors:</strong> Top 30 similar users
                    </p>
                    <p>
                      <strong>Prediction:</strong> Weighted average of similar users' ratings
                    </p>
                  </div>
                  <Badge variant="outline" className="bg-blue-50">
                    Memory-based approach
                  </Badge>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Item-Based Collaborative Filtering</CardTitle>
                  <CardDescription>Find similar items and recommend based on item relationships</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="text-sm text-gray-600">
                    <p>
                      <strong>Algorithm:</strong> Cosine similarity between items
                    </p>
                    <p>
                      <strong>Neighbors:</strong> Top 30 similar items
                    </p>
                    <p>
                      <strong>Prediction:</strong> Weighted average of similar items' ratings
                    </p>
                  </div>
                  <Badge variant="outline" className="bg-green-50">
                    More stable over time
                  </Badge>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Model Performance Comparison</CardTitle>
                <CardDescription>RMSE and MAE metrics for both models</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={modelPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="model" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="rmse" fill="#8884d8" name="RMSE" />
                    <Bar dataKey="mae" fill="#82ca9d" name="MAE" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="w-5 h-5" />
                  Train Collaborative Filtering Models
                </CardTitle>
                <CardDescription>
                  Build and evaluate both user-based and item-based recommendation models
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button onClick={() => runStep(3)} disabled={isRunning || activeStep < 3} className="w-full">
                  <Play className="w-4 h-4 mr-2" />
                  {isRunning ? "Training Models..." : "Start Model Training"}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Sample Recommendations */}
        {activeStep >= 4 && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="w-5 h-5" />
                Sample Recommendations
              </CardTitle>
              <CardDescription>Example recommendations for User #123</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium mb-3">User-Based CF Recommendations:</h4>
                  <div className="space-y-2">
                    {[
                      { item: "Movie 456", rating: 4.8 },
                      { item: "Movie 789", rating: 4.6 },
                      { item: "Movie 321", rating: 4.4 },
                      { item: "Movie 654", rating: 4.2 },
                      { item: "Movie 987", rating: 4.0 },
                    ].map((rec, index) => (
                      <div key={index} className="flex justify-between items-center p-2 bg-blue-50 rounded">
                        <span className="text-sm">{rec.item}</span>
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          <span className="text-sm font-medium">{rec.rating}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-3">Item-Based CF Recommendations:</h4>
                  <div className="space-y-2">
                    {[
                      { item: "Movie 234", rating: 4.7 },
                      { item: "Movie 567", rating: 4.5 },
                      { item: "Movie 890", rating: 4.3 },
                      { item: "Movie 123", rating: 4.1 },
                      { item: "Movie 456", rating: 3.9 },
                    ].map((rec, index) => (
                      <div key={index} className="flex justify-between items-center p-2 bg-green-50 rounded">
                        <span className="text-sm">{rec.item}</span>
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          <span className="text-sm font-medium">{rec.rating}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
