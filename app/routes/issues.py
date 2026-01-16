from fastapi import APIRouter, HTTPException, status

from app.schemas import IssueCreate, IssueOut, IssueUpdate, IssueStatus
from app.storage import load_data, save_data, update_data, delete_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get("/", response_model=list[IssueOut])
async def get_issues():
  """Retrieve all issues"""
  issues = load_data()
  return issues

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
  """Create new issue"""
  new_issue= {
    "title": payload.title,
    "description": payload.description,
    "priority": payload.priority,
    "status": IssueStatus.open
  }
  save_data(new_issue)
  return new_issue

@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
  """Retrieve a specific issue by Id"""
  issues = load_data()
  for issue in issues:
    if issue["id"] == issue_id:
      return issue
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
  """Update specific issue by Id"""
  issues = load_data()
  for _index, issue in enumerate(issues):
      if issue["id"] == int(issue_id):
        update_issue = issue.copy()
        if payload.title is not None:
          update_issue["title"] = payload.title
        if payload.description is not None:
          update_issue["description"] = payload.description
        if payload.priority is not None:
          update_issue["priority"] = payload.priority
        if payload.status is not None:
          update_issue["status"] = payload.status
        update_data(update_issue)
        return update_issue
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def get_issue(issue_id: str):
  """Delete a specific issue by Id"""
  res = delete_data(int(issue_id))
  if (res.data):
    return None
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
