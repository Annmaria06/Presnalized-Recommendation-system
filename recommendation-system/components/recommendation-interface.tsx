"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Star, Film, TrendingUp, Heart } from "lucide-react"

export default function RecommendationInterface() {
  const [selectedUser, setSelectedUser] = useState("")
  const [selectedModel, setSelectedModel] = useState("user-based")
  const [recommendations, setRecommendations] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const generateRecommendations = async () => {
    if (!selectedUser) return

    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      const mockRecommendations = [
        { id: 1, title: "The Shawshank Redemption", genre: "Drama", predicted_rating: 4.8, similarity: 0.92 },
        { id: 2, title: "Pulp Fiction", genre: "Crime", predicted_rating: 4.6, similarity: 0.89 },
        { id: 3, title: "The Dark Knight", genre: "Action", predicted_rating: 4.5, similarity: 0.87 },
        { id: 4, title: "Forrest Gump", genre: "Drama", predicted_rating: 4.4, similarity: 0.85 },
        { id: 5, title: "Inception", genre: "Sci-Fi", predicted_rating: 4.3, similarity: 0.83 },
        { id: 6, title: "The Matrix", genre: "Sci-Fi", predicted_rating: 4.2, similarity: 0.81 },
        { id: 7, title: "Goodfellas", genre: "Crime", predicted_rating: 4.1, similarity: 0.79 },
        { id: 8, title: "The Godfather", genre: "Crime", predicted_rating: 4.0, similarity: 0.77 },
      ]

      setRecommendations(mockRecommendations)
      setIsLoading(false)
    }, 1500)
  }

  const getGenreColor = (genre) => {
    const colors = {
      Drama: "bg-blue-100 text-blue-800",
      Crime: "bg-red-100 text-red-800",
      Action: "bg-orange-100 text-orange-800",
      "Sci-Fi": "bg-purple-100 text-purple-800",
      Comedy: "bg-green-100 text-green-800",
      Romance: "bg-pink-100 text-pink-800",
    }
    return colors[genre] || "bg-gray-100 text-gray-800"
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Movie Recommendation System
          </CardTitle>
          <CardDescription>Get personalized movie recommendations using collaborative filtering</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="user-id">User ID</Label>
              <Input
                id="user-id"
                placeholder="Enter user ID (1-943)"
                value={selectedUser}
                onChange={(e) => setSelectedUser(e.target.value)}
                type="number"
                min="1"
                max="943"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="model-type">Recommendation Model</Label>
              <Select value={selectedModel} onValueChange={setSelectedModel}>
                <SelectTrigger>
                  <SelectValue placeholder="Select model" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="user-based">User-Based CF</SelectItem>
                  <SelectItem value="item-based">Item-Based CF</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-end">
              <Button onClick={generateRecommendations} disabled={!selectedUser || isLoading} className="w-full">
                {isLoading ? "Generating..." : "Get Recommendations"}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Film className="w-5 h-5" />
              Recommended Movies for User {selectedUser}
            </CardTitle>
            <CardDescription>
              Based on {selectedModel === "user-based" ? "similar users" : "similar items"} preferences
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4">
              {recommendations.map((movie, index) => (
                <div
                  key={movie.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">{movie.title}</h3>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge className={getGenreColor(movie.genre)}>{movie.genre}</Badge>
                        <span className="text-sm text-gray-500">
                          Similarity: {(movie.similarity * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1">
                      <Star className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                      <span className="font-semibold text-lg">{movie.predicted_rating}</span>
                    </div>
                    <Button variant="outline" size="sm">
                      <Heart className="w-4 h-4 mr-1" />
                      Save
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Model Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">User-Based Collaborative Filtering</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm text-gray-600">
              <p>
                <strong>How it works:</strong> Finds users with similar rating patterns and recommends movies they
                liked.
              </p>
              <p>
                <strong>Best for:</strong> Users with many ratings and clear preferences.
              </p>
              <p>
                <strong>Advantages:</strong> Captures user taste evolution, good for niche items.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline">RMSE: 0.92</Badge>
              <Badge variant="outline">MAE: 0.73</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Item-Based Collaborative Filtering</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm text-gray-600">
              <p>
                <strong>How it works:</strong> Finds movies similar to ones you've rated highly and recommends related
                items.
              </p>
              <p>
                <strong>Best for:</strong> New users or when item relationships are stable over time.
              </p>
              <p>
                <strong>Advantages:</strong> More stable recommendations, better performance with sparse data.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline">RMSE: 0.89</Badge>
              <Badge variant="outline">MAE: 0.71</Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Usage Instructions */}
      <Card>
        <CardHeader>
          <CardTitle>How to Use This System</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold mb-2">Getting Started:</h4>
              <ol className="text-sm text-gray-600 space-y-1 list-decimal list-inside">
                <li>Enter a User ID between 1 and 943</li>
                <li>Choose your preferred recommendation model</li>
                <li>Click "Get Recommendations" to see personalized suggestions</li>
                <li>Explore different users to see how preferences vary</li>
              </ol>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Understanding Results:</h4>
              <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
                <li>Higher predicted ratings indicate stronger recommendations</li>
                <li>Similarity percentage shows how confident the model is</li>
                <li>Genre badges help identify recommendation patterns</li>
                <li>Rankings are ordered by predicted preference</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
